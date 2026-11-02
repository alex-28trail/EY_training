
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from psycopg2.extras import RealDictCursor

from database import get_db_connection
from auth import get_current_user


router = APIRouter(
    prefix="/providers",
    tags=["Provider Management"]
)


# Request models

class BreakItem(BaseModel):
    start_time: time
    end_time: time


class ScheduleItem(BaseModel):
    day_of_week: int = Field(ge=0, le=6)
    start_time: time
    end_time: time
    breaks: list[BreakItem] = Field(default_factory=list)


class ScheduleUpdate(BaseModel):
    schedules: list[ScheduleItem]


class UnavailabilityRequest(BaseModel):
    start_at: datetime
    end_at: datetime
    reason: str | None = None


# Get the logged-in provider

def get_current_provider(user=Depends(get_current_user)):

    if user["role"] != "PROVIDER":
        raise HTTPException(
            status_code=403,
            detail="Provider access required"
        )

    connection = get_db_connection()

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            """
            SELECT id, name, timezone
            FROM providers
            WHERE user_id = %s
              AND is_active = TRUE
            """,
            (user["id"],)
        )

        provider = cursor.fetchone()
        cursor.close()

        if not provider:
            raise HTTPException(
                status_code=404,
                detail="Provider profile not found"
            )

        return provider

    finally:
        connection.close()


# Validate weekly schedule

def validate_schedule(schedules):

    for schedule in schedules:

        if schedule.start_time >= schedule.end_time:
            raise HTTPException(
                status_code=400,
                detail="Schedule end time must be after start time"
            )

        for break_item in schedule.breaks:

            if not (
                schedule.start_time <= break_item.start_time
                < break_item.end_time <= schedule.end_time
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Breaks must be within working hours"
                )

        for i, first_break in enumerate(schedule.breaks):
            for second_break in schedule.breaks[i + 1:]:

                if (
                    first_break.start_time < second_break.end_time
                    and second_break.start_time < first_break.end_time
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="Breaks cannot overlap"
                    )

    for i, first in enumerate(schedules):
        for second in schedules[i + 1:]:

            if first.day_of_week == second.day_of_week:

                if (
                    first.start_time < second.end_time
                    and second.start_time < first.end_time
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="Working hours cannot overlap"
                    )


# GET: View provider weekly schedule

@router.get("/me/schedule")
def get_my_schedule(
    provider=Depends(get_current_provider)
):
    connection = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            """
            SELECT id, day_of_week, start_time, end_time, is_active
            FROM provider_schedules
            WHERE provider_id = %s
            ORDER BY day_of_week, start_time
            """,
            (provider["id"],)
        )

        schedules = cursor.fetchall()

        for schedule in schedules:

            cursor.execute(
                """
                SELECT id, start_time, end_time
                FROM provider_schedule_breaks
                WHERE schedule_id = %s
                ORDER BY start_time
                """,
                (schedule["id"],)
            )

            schedule["breaks"] = cursor.fetchall()

        cursor.close()

        return {
            "provider_id": provider["id"],
            "provider_name": provider["name"],
            "timezone": provider["timezone"],
            "schedules": schedules
        }

    finally:
        if connection:
            connection.close()


# PUT: Update provider weekly schedule

@router.put("/me/schedule")
def update_my_schedule(
    request: ScheduleUpdate,
    provider=Depends(get_current_provider)
):
    validate_schedule(request.schedules)

    connection = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            """
            SELECT
                a.appointment_date,
                a.start_time,
                a.end_time
            FROM appointments a
            JOIN services s ON s.id = a.service_id
            WHERE s.provider_id = %s
              AND a.status = 'Confirmed'
              AND a.appointment_date >= CURRENT_DATE
            """,
            (provider["id"],)
        )

        appointments = cursor.fetchall()

        for appointment in appointments:

            weekday = appointment["appointment_date"].weekday()

            matching_schedules = [
                item for item in request.schedules
                if item.day_of_week == weekday
                and item.start_time <= appointment["start_time"]
                and item.end_time >= appointment["end_time"]
            ]

            valid_booking = False

            for schedule in matching_schedules:

                overlaps_break = any(
                    appointment["start_time"] < break_item.end_time
                    and appointment["end_time"] > break_item.start_time
                    for break_item in schedule.breaks
                )

                if not overlaps_break:
                    valid_booking = True
                    break

            if not valid_booking:
                raise HTTPException(
                    status_code=409,
                    detail=(
                        "Schedule cannot be changed because it would "
                        "affect an existing confirmed appointment."
                    )
                )

        cursor.execute(
            """
            DELETE FROM provider_schedules
            WHERE provider_id = %s
            """,
            (provider["id"],)
        )

        for schedule in request.schedules:

            cursor.execute(
                """
                INSERT INTO provider_schedules (
                    provider_id,
                    day_of_week,
                    start_time,
                    end_time,
                    is_active
                )
                VALUES (%s, %s, %s, %s, TRUE)
                RETURNING id
                """,
                (
                    provider["id"],
                    schedule.day_of_week,
                    schedule.start_time,
                    schedule.end_time
                )
            )

            schedule_id = cursor.fetchone()["id"]

            for break_item in schedule.breaks:

                cursor.execute(
                    """
                    INSERT INTO provider_schedule_breaks (
                        schedule_id,
                        start_time,
                        end_time
                    )
                    VALUES (%s, %s, %s)
                    """,
                    (
                        schedule_id,
                        break_item.start_time,
                        break_item.end_time
                    )
                )

        connection.commit()
        cursor.close()

        return {
            "message": "Provider schedule updated successfully",
            "provider_id": provider["id"],
            "schedules_saved": len(request.schedules)
        }

    except HTTPException:
        if connection:
            connection.rollback()
        raise

    except Exception:
        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Unable to update provider schedule"
        )

    finally:
        if connection:
            connection.close()


# POST: Add provider unavailability

@router.post("/me/unavailability", status_code=201)
def add_unavailability(
    request: UnavailabilityRequest,
    provider=Depends(get_current_provider)
):

    if (
        request.start_at.tzinfo is None
        or request.end_at.tzinfo is None
    ):
        raise HTTPException(
            status_code=400,
            detail="Start and end times must include a timezone"
        )

    if request.start_at >= request.end_at:
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time"
        )

    if request.start_at <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="Unavailability must start in the future"
        )

    connection = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        provider_timezone = ZoneInfo(provider["timezone"])

        start_local = request.start_at.astimezone(provider_timezone)
        end_local = request.end_at.astimezone(provider_timezone)

        cursor.execute(
            """
            SELECT
                a.appointment_date,
                a.start_time,
                a.end_time
            FROM appointments a
            JOIN services s ON s.id = a.service_id
            WHERE s.provider_id = %s
              AND a.status = 'Confirmed'
              AND a.appointment_date BETWEEN %s AND %s
            """,
            (
                provider["id"],
                start_local.date(),
                end_local.date()
            )
        )

        appointments = cursor.fetchall()

        for appointment in appointments:

            appointment_start = datetime.combine(
                appointment["appointment_date"],
                appointment["start_time"],
                tzinfo=provider_timezone
            )

            appointment_end = datetime.combine(
                appointment["appointment_date"],
                appointment["end_time"],
                tzinfo=provider_timezone
            )

            if (
                request.start_at < appointment_end
                and request.end_at > appointment_start
            ):
                raise HTTPException(
                    status_code=409,
                    detail="This period overlaps an existing appointment"
                )

        cursor.execute(
            """
            SELECT id
            FROM provider_unavailability
            WHERE provider_id = %s
              AND start_at < %s
              AND end_at > %s
            """,
            (
                provider["id"],
                request.end_at,
                request.start_at
            )
        )

        if cursor.fetchone():
            raise HTTPException(
                status_code=409,
                detail="This period overlaps existing unavailability"
            )

        cursor.execute(
            """
            INSERT INTO provider_unavailability (
                provider_id,
                start_at,
                end_at,
                reason
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id, start_at, end_at, reason
            """,
            (
                provider["id"],
                request.start_at,
                request.end_at,
                request.reason
            )
        )

        result = cursor.fetchone()

        connection.commit()
        cursor.close()

        return {
            "message": "Unavailability added successfully",
            "unavailability": result
        }

    except HTTPException:
        if connection:
            connection.rollback()
        raise

    except Exception:
        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Unable to add unavailability"
        )

    finally:
        if connection:
            connection.close()


# DELETE: Remove provider unavailability

@router.delete("/me/unavailability/{unavailability_id}")
def delete_unavailability(
    unavailability_id: int,
    provider=Depends(get_current_provider)
):
    connection = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM provider_unavailability
            WHERE id = %s
              AND provider_id = %s
            RETURNING id
            """,
            (unavailability_id, provider["id"])
        )

        deleted_record = cursor.fetchone()

        if not deleted_record:
            raise HTTPException(
                status_code=404,
                detail="Unavailability record not found"
            )

        connection.commit()
        cursor.close()

        return {
            "message": "Unavailability removed successfully",
            "id": deleted_record[0]
        }

    except HTTPException:
        if connection:
            connection.rollback()
        raise

    except Exception:
        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Unable to remove unavailability"
        )

    finally:
        if connection:
            connection.close()


# GET: Generate available appointment slots

@router.get("/{provider_id}/availability")
def get_provider_availability(
    provider_id: int,
    service_id: int = Query(gt=0),
    selected_date: date = Query(alias="date"),
):
    connection = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Get provider details

        cursor.execute(
            """
            SELECT id, name, timezone
            FROM providers
            WHERE id = %s
              AND is_active = TRUE
            """,
            (provider_id,)
        )

        provider = cursor.fetchone()

        if not provider:
            raise HTTPException(
                status_code=404,
                detail="Provider not found"
            )

        provider_timezone = ZoneInfo(provider["timezone"])
        now_local = datetime.now(provider_timezone)

        if selected_date < now_local.date():
            raise HTTPException(
                status_code=400,
                detail="Cannot check availability for a past date"
            )

        # Get selected service

        cursor.execute(
            """
            SELECT id, name, duration_minutes, price
            FROM services
            WHERE id = %s
              AND provider_id = %s
              AND is_active = TRUE
            """,
            (service_id, provider_id)
        )

        service = cursor.fetchone()

        if not service:
            raise HTTPException(
                status_code=404,
                detail="Service not found for this provider"
            )

        # Get configured slot interval

        cursor.execute(
            """
            SELECT setting_value
            FROM system_settings
            WHERE setting_key = 'slot_interval_minutes'
            """
        )

        setting = cursor.fetchone()

        if not setting:
            raise HTTPException(
                status_code=500,
                detail="Slot interval setting is missing"
            )

        slot_interval = int(setting["setting_value"])

        if slot_interval <= 0:
            raise HTTPException(
                status_code=500,
                detail="Invalid slot interval configuration"
            )

        # Get provider working hours

        cursor.execute(
            """
            SELECT id, start_time, end_time
            FROM provider_schedules
            WHERE provider_id = %s
              AND day_of_week = %s
              AND is_active = TRUE
            ORDER BY start_time
            """,
            (provider_id, selected_date.weekday())
        )

        schedules = cursor.fetchall()

        if not schedules:
            return {
                "provider_id": provider_id,
                "provider_name": provider["name"],
                "service": service,
                "date": selected_date,
                "timezone": provider["timezone"],
                "slot_interval_minutes": slot_interval,
                "available_slots": []
            }

        # Get breaks for all working periods

        breaks = []

        for schedule in schedules:

            cursor.execute(
                """
                SELECT start_time, end_time
                FROM provider_schedule_breaks
                WHERE schedule_id = %s
                """,
                (schedule["id"],)
            )

            breaks.extend(cursor.fetchall())

        # Get existing confirmed appointments

        cursor.execute(
            """
            SELECT a.start_time, a.end_time
            FROM appointments a
            JOIN services s ON s.id = a.service_id
            WHERE s.provider_id = %s
              AND a.appointment_date = %s
              AND a.status = 'Confirmed'
            """,
            (provider_id, selected_date)
        )

        appointments = cursor.fetchall()

        # Get unavailable periods for this date

        day_start = datetime.combine(
            selected_date,
            time.min,
            tzinfo=provider_timezone
        )

        day_end = day_start + timedelta(days=1)

        cursor.execute(
            """
            SELECT start_at, end_at
            FROM provider_unavailability
            WHERE provider_id = %s
              AND start_at < %s
              AND end_at > %s
            """,
            (provider_id, day_end, day_start)
        )

        unavailable_periods = cursor.fetchall()

        # Generate available slots

        available_slots = []
        service_duration = timedelta(
            minutes=service["duration_minutes"]
        )

        slot_interval_delta = timedelta(
            minutes=slot_interval
        )

        for schedule in schedules:

            slot_start = datetime.combine(
                selected_date,
                schedule["start_time"],
                tzinfo=provider_timezone
            )

            working_end = datetime.combine(
                selected_date,
                schedule["end_time"],
                tzinfo=provider_timezone
            )

            while slot_start + service_duration <= working_end:

                slot_end = slot_start + service_duration

                # Exclude past slots

                if slot_start <= now_local:
                    slot_start += slot_interval_delta
                    continue

                # Check break overlap

                overlaps_break = any(
                    slot_start.time() < break_item["end_time"]
                    and slot_end.time() > break_item["start_time"]
                    for break_item in breaks
                )

                # Check appointment overlap

                overlaps_appointment = any(
                    slot_start.time() < appointment["end_time"]
                    and slot_end.time() > appointment["start_time"]
                    for appointment in appointments
                )

                # Check unavailable period overlap

                overlaps_unavailability = any(
                    slot_start < unavailable["end_at"]
                    and slot_end > unavailable["start_at"]
                    for unavailable in unavailable_periods
                )

                if not (
                    overlaps_break
                    or overlaps_appointment
                    or overlaps_unavailability
                ):
                    available_slots.append({
                        "start_at": slot_start.isoformat(),
                        "end_at": slot_end.isoformat()
                    })

                slot_start += slot_interval_delta

        cursor.close()

        return {
            "provider_id": provider_id,
            "provider_name": provider["name"],
            "service": service,
            "date": selected_date,
            "timezone": provider["timezone"],
            "slot_interval_minutes": slot_interval,
            "available_slots": available_slots
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to generate available appointment slots"
        )

    finally:
        if connection:
            connection.close()
