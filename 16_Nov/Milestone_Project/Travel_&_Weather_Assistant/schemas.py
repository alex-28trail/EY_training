
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    response: str
    session_id: str


class TripRequest(BaseModel):
    origin: str
    destination: str
    departure_date: date
    return_date: Optional[date] = None
    travelers: int = Field(default=1, ge=1)
    preferences: Optional[str] = None


class WeatherRequest(BaseModel):
    city: str
    forecast_date: Optional[date] = None


class TripResponse(BaseModel):
    trip_id: int
    origin: str
    destination: str
    departure_date: date
    return_date: Optional[date] = None
    travelers: int
    message: str
