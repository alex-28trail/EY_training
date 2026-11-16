
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from schemas import (
    ChatRequest,
    ChatResponse,
    TripRequest,
    TripResponse,
    WeatherRequest
)

from database.database import initialize_database

from assistant.workflow import process_message
from assistant.llm import check_model_connection
from assistant.memory import check_redis_connection

from tools.weather_tools import get_weather

from tools.trip_tools import (
    create_travel_plan,
    list_travel_plans,
    get_travel_plan
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the database when the application starts."""

    initialize_database()
    yield


app = FastAPI(
    title="Travel and Weather Assistant",
    description="An AI-powered assistant for travel planning and weather information.",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
def home():
    """Application home endpoint."""

    return {
        "message": "Welcome to the Travel and Weather Assistant API!",
        "status": "running",
        "documentation": "/docs"
    }


@app.get("/health")
def health_check():
    """Check the status of application services."""

    return {
        "application": "running",
        "ollama": check_model_connection(),
        "redis": check_redis_connection()
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Send a message to the AI assistant."""

    response = process_message(
        message=request.message,
        session_id=request.session_id
    )

    return ChatResponse(
        response=response,
        session_id=request.session_id
    )


@app.post("/weather")
def weather(request: WeatherRequest):
    """Get current weather or a forecast."""

    result = get_weather(
        city=request.city,
        forecast_date=(
            request.forecast_date.isoformat()
            if request.forecast_date else None
        )
    )

    if "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result


@app.post("/trips", response_model=TripResponse)
def create_trip(request: TripRequest):
    """Create and save a travel plan."""

    result = create_travel_plan(
        origin=request.origin,
        destination=request.destination,
        departure_date=request.departure_date.isoformat(),
        return_date=(
            request.return_date.isoformat()
            if request.return_date else None
        ),
        travelers=request.travelers,
        preferences=request.preferences
    )

    if "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return TripResponse(
        trip_id=result["trip_id"],
        origin=result["origin"],
        destination=result["destination"],
        departure_date=request.departure_date,
        return_date=request.return_date,
        travelers=result["travelers"],
        message=result["message"]
    )


@app.get("/trips")
def get_all_trips():
    """Retrieve all saved travel plans."""

    return list_travel_plans()


@app.get("/trips/{trip_id}")
def get_trip(trip_id: int):
    """Retrieve a specific travel plan."""

    result = get_travel_plan(trip_id)

    if "error" in result:
        raise HTTPException(
            status_code=404,
            detail=result["error"]
        )

    return result
