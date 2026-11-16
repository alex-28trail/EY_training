
import re
import json

from assistant.llm import generate_response
from assistant.memory import add_message, get_history

from tools.trip_tools import (
    create_travel_plan,
    list_travel_plans,
    get_travel_plan
)

from tools.weather_tools import get_weather


SYSTEM_PROMPT = """
You are a helpful Travel and Weather Assistant.

Your responsibilities:
1. Help users plan and manage trips.
2. Provide current weather information and forecasts.
3. Answer general travel-related questions.
4. Remember previous conversation context when available.

Guidelines:
- Be friendly, clear, and concise.
- Ask for missing information when necessary.
- Never invent weather information or trip details.
- Format dates clearly.
- If a tool returns an error, explain it to the user.
"""


def detect_intent(message: str) -> str:
    """Identify the user's intent."""

    text = message.lower()

    if any(word in text for word in [
        "weather", "forecast", "temperature",
        "rain", "rainfall", "humidity"
    ]):
        return "weather"

    if any(word in text for word in [
        "my trips", "list trips", "show trips",
        "all trips", "saved trips"
    ]):
        return "list_trips"

    if re.search(r"\btrip\s+(?:id\s*)?#?\d+\b", text):
        return "get_trip"

    if any(word in text for word in [
        "plan a trip", "create a trip",
        "save a trip", "plan my trip"
    ]):
        return "create_trip"

    return "general"


def extract_weather_details(message: str):
    """Extract city, country, and forecast date."""

    city_match = re.search(
        r"(?:weather|forecast|temperature)\s+"
        r"(?:in|for|at)\s+([A-Za-z\s]+?)(?:,|\s+on\s+|\s+for\s+|$)",
        message,
        re.IGNORECASE
    )

    if not city_match:
        city_match = re.search(
            r"(?:in|for)\s+([A-Za-z\s]+?)(?:,|\s+on\s+|\s+for\s+|$)",
            message,
            re.IGNORECASE
        )

    if not city_match:
        return None

    city = city_match.group(1).strip()

    country_match = re.search(
        r",\s*([A-Za-z\s]+?)(?:\s+on\s+|\s+for\s+|$)",
        message,
        re.IGNORECASE
    )

    country = country_match.group(1).strip() if country_match else None

    date_match = re.search(
        r"\b\d{4}-\d{2}-\d{2}\b",
        message
    )

    forecast_date = date_match.group(0) if date_match else None

    return {
        "city": city,
        "country": country,
        "forecast_date": forecast_date
    }


def extract_trip_details(message: str):
    """Extract trip information from a user message."""

    match = re.search(
        r"from\s+(.+?)\s+to\s+(.+?)\s+on\s+(\d{4}-\d{2}-\d{2})",
        message,
        re.IGNORECASE
    )

    if not match:
        return None

    origin = match.group(1).strip()
    destination = match.group(2).strip()
    departure_date = match.group(3)

    return {
        "origin": origin,
        "destination": destination,
        "departure_date": departure_date,
        "return_date": None,
        "travelers": 1,
        "preferences": None
    }


def build_conversation_context(session_id: str) -> str:
    """Build context from previous conversation messages."""

    history = get_history(session_id)

    if not history:
        return ""

    conversation = []

    for item in history[-10:]:
        role = item["role"].capitalize()
        content = item["content"]

        conversation.append(f"{role}: {content}")

    return "\n".join(conversation)


def process_message(
    message: str,
    session_id: str = "default"
) -> str:
    """Process a user message and return the assistant response."""

    if not message or not message.strip():
        return "Please enter a message."

    message = message.strip()

    try:
        add_message(session_id, "user", message)

        intent = detect_intent(message)

        tool_result = None

        # Weather assistance
        if intent == "weather":

            details = extract_weather_details(message)

            if details:
                tool_result = get_weather(
                    city=details["city"],
                    country=details["country"],
                    forecast_date=details["forecast_date"]
                )
            else:
                tool_result = {
                    "message": (
                        "Please specify a city. "
                        "For example: What is the weather in Bengaluru, India?"
                    )
                }

        # Create a travel plan
        elif intent == "create_trip":

            details = extract_trip_details(message)

            if details:
                tool_result = create_travel_plan(**details)
            else:
                tool_result = {
                    "message": (
                        "To create a trip, please provide your origin, "
                        "destination, and departure date. "
                        "Example: Plan a trip from Delhi to Mumbai "
                        "on 2026-12-10."
                    )
                }

        # Retrieve all saved trips
        elif intent == "list_trips":

            tool_result = list_travel_plans()

        # Retrieve one saved trip
        elif intent == "get_trip":

            match = re.search(
                r"\btrip\s+(?:id\s*)?#?(\d+)\b",
                message,
                re.IGNORECASE
            )

            if match:
                trip_id = int(match.group(1))
                tool_result = get_travel_plan(trip_id)

        # Build conversation context
        context = build_conversation_context(session_id)

        if tool_result is not None:

            prompt = f"""
Previous conversation:
{context}

User request:
{message}

Tool result:
{json.dumps(tool_result, default=str, indent=2)}

Respond naturally based on the tool result.
Do not invent information that is not present in the result.
"""

        else:

            prompt = f"""
Previous conversation:
{context}

User request:
{message}

Respond helpfully using the conversation context.
"""

        response = generate_response(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT
        )

        add_message(session_id, "assistant", response)

        return response

    except Exception as error:
        print(f"Workflow error: {error}")
        return "Sorry, something went wrong while processing your request."
