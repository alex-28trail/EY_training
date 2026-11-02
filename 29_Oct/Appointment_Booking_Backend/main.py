
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.extras import RealDictCursor

from database import get_db_connection
from auth import router as auth_router, get_current_user
from provider_routes import router as provider_router


app = FastAPI(
    title="Appointment Booking API",
    description="Backend for the Appointment Booking System",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(auth_router)
app.include_router(provider_router)


@app.get("/")
def home():
    return {"message": "Appointment Booking API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/db-health")
def database_health_check():
    connection = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT current_database(), version()"
        )

        result = cursor.fetchone()
        cursor.close()

        return {
            "status": "connected",
            "database": result[0],
            "postgresql_version": result[1]
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        )

    finally:
        if connection:
            connection.close()


@app.get("/providers")
def get_providers():
    connection = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute("""
            SELECT id, name, specialty, description
            FROM providers
            ORDER BY id
        """)

        providers = cursor.fetchall()
        cursor.close()

        return providers

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve providers"
        )

    finally:
        if connection:
            connection.close()


@app.get("/services")
def get_services():
    connection = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute("""
            SELECT
                s.id,
                s.provider_id,
                p.name AS provider_name,
                s.name,
                s.description,
                s.duration_minutes,
                s.price
            FROM services s
            JOIN providers p ON s.provider_id = p.id
            ORDER BY s.id
        """)

        services = cursor.fetchall()
        cursor.close()

        return services

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve services"
        )

    finally:
        if connection:
            connection.close()


@app.get("/providers/{provider_id}/services")
def get_provider_services(provider_id: int):
    connection = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute(
            """
            SELECT id, name, specialty
            FROM providers
            WHERE id = %s
            """,
            (provider_id,)
        )

        provider = cursor.fetchone()

        if not provider:
            raise HTTPException(
                status_code=404,
                detail="Provider not found"
            )

        cursor.execute("""
            SELECT
                id,
                provider_id,
                name,
                description,
                duration_minutes,
                price
            FROM services
            WHERE provider_id = %s
            ORDER BY id
        """, (provider_id,))

        services = cursor.fetchall()
        cursor.close()

        return {
            "provider": provider,
            "services": services
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve provider services"
        )

    finally:
        if connection:
            connection.close()


@app.get("/auth/me")
def get_my_profile(user=Depends(get_current_user)):
    return user
