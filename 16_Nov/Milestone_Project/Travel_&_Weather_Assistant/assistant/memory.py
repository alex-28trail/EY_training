
import json
import os

import redis
from dotenv import load_dotenv


load_dotenv()

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0"
)

# Connect to Redis
redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True
)

# Conversation history expiration: 24 hours
MEMORY_TTL = 86400


def add_message(session_id: str, role: str, content: str):
    """Save a message to a conversation session."""

    key = f"travel_assistant:{session_id}"

    message = {
        "role": role,
        "content": content
    }

    redis_client.rpush(key, json.dumps(message))
    redis_client.expire(key, MEMORY_TTL)


def get_history(session_id: str):
    """Retrieve conversation history for a session."""

    key = f"travel_assistant:{session_id}"

    messages = redis_client.lrange(key, 0, -1)

    return [
        json.loads(message)
        for message in messages
    ]


def clear_history(session_id: str):
    """Delete conversation history for a session."""

    key = f"travel_assistant:{session_id}"

    redis_client.delete(key)

    return {
        "message": "Conversation history cleared successfully."
    }


def check_redis_connection() -> bool:
    """Check whether Redis is available."""

    try:
        return redis_client.ping()
    except redis.RedisError as error:
        print(f"Redis connection error: {error}")
        return False
