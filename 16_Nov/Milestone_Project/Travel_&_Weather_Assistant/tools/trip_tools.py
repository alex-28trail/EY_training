
from database.database import (
    create_trip,
    get_all_trips,
    get_trip_by_id
)


def create_travel_plan(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: str = None,
    travelers: int = 1,
    preferences: str = None
):
    """Create and save a new travel plan."""

    if not origin.strip() or not destination.strip():
        return {"error": "Origin and destination are required."}

    if travelers < 1:
        return {"error": "At least one traveler is required."}

    trip_id = create_trip(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date,
        travelers=travelers,
        preferences=preferences
    )

    return {
        "message": "Travel plan created successfully!",
        "trip_id": trip_id,
        "origin": origin,
        "destination": destination,
        "departure_date": departure_date,
        "return_date": return_date,
        "travelers": travelers,
        "preferences": preferences
    }


def list_travel_plans():
    """Retrieve all saved travel plans."""

    trips = get_all_trips()

    if not trips:
        return {"message": "No travel plans found.", "trips": []}

    return {
        "total_trips": len(trips),
        "trips": trips
    }


def get_travel_plan(trip_id: int):
    """Retrieve a travel plan using its ID."""

    trip = get_trip_by_id(trip_id)

    if not trip:
        return {"error": f"No travel plan found with ID {trip_id}."}

    return trip
