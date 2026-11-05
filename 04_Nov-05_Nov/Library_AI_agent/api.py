
"""FastAPI backend for the AI Library Assistant."""

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from tools import reserve_book
from agent import answer_api_turn


BASE_DIR = Path(__file__).resolve().parent

BOOKS_FILE = BASE_DIR / "books.json"
RESERVATIONS_FILE = BASE_DIR / "reservations.json"


app = FastAPI(
    title="AI Library Assistant API",
    description="Backend API for the AI Library Assistant",
    version="2.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReservationRequest(BaseModel):
    book_id: int
    customer_name: str = Field(min_length=1, max_length=100)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]


def read_json(file_path):
    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


@app.get("/")
def home():
    return {
        "message": "AI Library Assistant API is running"
    }


@app.get("/books")
def get_books():
    books = read_json(BOOKS_FILE)

    return {
        "total_books": len(books),
        "books": books
    }


@app.get("/reservations")
def get_reservations():
    reservations = read_json(RESERVATIONS_FILE)

    return {
        "total_reservations": len(reservations),
        "reservations": reservations
    }


@app.post("/reservations/preview")
def preview_reservation(request: ReservationRequest):
    customer_name = request.customer_name.strip()

    if not customer_name:
        raise HTTPException(
            status_code=400,
            detail="Customer name cannot be empty."
        )

    books = read_json(BOOKS_FILE)

    selected_book = next(
        (book for book in books if book["id"] == request.book_id),
        None
    )

    if selected_book is None:
        raise HTTPException(status_code=404, detail="Book not found.")

    if selected_book["available_copies"] <= 0:
        raise HTTPException(
            status_code=400,
            detail="This book is currently unavailable."
        )

    return {
        "success": True,
        "message": "Book is available for reservation.",
        "book": selected_book,
        "customer_name": customer_name
    }


@app.post("/reservations")
def create_reservation(request: ReservationRequest):
    customer_name = request.customer_name.strip()

    if not customer_name:
        raise HTTPException(
            status_code=400,
            detail="Customer name cannot be empty."
        )

    result = reserve_book(
        book_id=request.book_id,
        customer_name=customer_name,
        confirmed=True
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["message"]
        )

    return result


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        messages = [
            message.model_dump()
            for message in request.messages
        ]

        if not messages or messages[-1]["role"] != "user":
            raise HTTPException(
                status_code=400,
                detail="A user message is required."
            )

        result = answer_api_turn(messages)

        return {
            "success": True,
            "reply": result["reply"],
            "pending_reservation": result["pending_reservation"]
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"AI assistant error: {str(exc)}"
        )
