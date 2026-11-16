
# Time & Weather Assistant

An AI-powered Travel and Weather Assistant built using Python, FastAPI, Ollama, Redis, and SQLite.

The assistant allows users to interact through natural language to manage travel plans, retrieve weather information, and maintain conversation history.

## Features

- AI-powered conversational assistant using Ollama.
- Current weather information for cities.
- Weather forecasts for selected dates.
- Create and save travel plans.
- Retrieve all saved travel plans.
- Retrieve individual trips using trip IDs.
- Conversation memory using Redis.
- SQLite database for persistent trip storage.
- REST API built with FastAPI.
- Interactive API documentation using Swagger UI.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API development |
| Ollama | Local LLM integration |
| Qwen 2.5 3B | Language model |
| Redis | Conversation memory |
| SQLite | Trip database |
| Open-Meteo | Weather information |
| Pydantic | Request validation |

## Project Structure

```text
Time_&_Weather_Assistant/
│
├── database/
│   └── database.py
│
├── tools/
│   ├── trip_tools.py
│   └── weather_tools.py
│
├── assistant/
│   ├── llm.py
│   ├── workflow.py
│   └── memory.py
│
├── main.py
├── schemas.py
├── requirements.txt
├── .env.example
├── README.md
└── travel.db
```

## Prerequisites

Install the following before running the project:

- Python 3.10 or later
- Ollama
- Docker Desktop

## Swagger AI URL
http://127.0.0.1:8000/docs?utm_source=chatgpt.com