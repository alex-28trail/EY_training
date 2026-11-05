
"""Python tools for the AI Library Assistant."""

import json
from pathlib import Path
from datetime import datetime


ROOT = Path(__file__).resolve().parent

BOOKS_FILE = ROOT / "books.json"
RESERVATIONS_FILE = ROOT / "reservations.json"


def load_json(file_path):
    """Read data from a JSON file."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(file_path, data):
    """Write data into a JSON file."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def search_books(keyword: str) -> dict:
    """Search books by title, author, or category."""

    books = load_json(BOOKS_FILE)
    keyword = keyword.strip().lower()

    if not keyword:
        return {
            "success": False,
            "message": "Please provide a search keyword.",
            "books": []
        }

    matching_books = []

    for book in books:
        searchable_text = (
            book["title"] + " " +
            book["author"] + " " +
            book["category"]
        ).lower()

        if keyword in searchable_text:
            matching_books.append({
                "id": book["id"],
                "title": book["title"],
                "author": book["author"],
                "category": book["category"],
                "available_copies": book["available_copies"],
                "availability": (
                    "Available"
                    if book["available_copies"] > 0
                    else "Out of stock"
                )
            })

    return {
        "success": True,
        "total_results": len(matching_books),
        "books": matching_books,
        "message": (
            f"Found {len(matching_books)} matching book(s)."
            if matching_books
            else f"No books found for '{keyword}'."
        )
    }


def preview_reservation(book_id: int, customer_name: str) -> dict:
    """Check reservation details without changing any JSON data."""

    books = load_json(BOOKS_FILE)
    customer_name = customer_name.strip()

    if not customer_name:
        return {
            "success": False,
            "message": "Please provide the customer's name."
        }

    selected_book = next(
        (book for book in books if book["id"] == book_id),
        None
    )

    if selected_book is None:
        return {
            "success": False,
            "message": "Book not found."
        }

    if selected_book["available_copies"] <= 0:
        return {
            "success": False,
            "message": f"'{selected_book['title']}' is currently unavailable."
        }

    return {
        "success": True,
        "confirmation_required": True,
        "message": "The book is available. Please confirm the reservation.",
        "book": selected_book,
        "customer_name": customer_name
    }


def reserve_book(
    book_id: int,
    customer_name: str,
    confirmed: bool | None = None
) -> dict:
    """Reserve a book after checking availability.

    confirmed=None: Ask for confirmation in the terminal.
    confirmed=False: Cancel the reservation.
    confirmed=True: Complete the reservation.
    """

    preview = preview_reservation(book_id, customer_name)

    if not preview["success"]:
        return {
            "success": False,
            "created": False,
            "message": preview["message"]
        }

    selected_book = preview["book"]
    customer_name = customer_name.strip()

    if confirmed is None:
        print("\n" + "=" * 45)
        print("          RESERVATION CONFIRMATION")
        print("=" * 45)
        print("Book ID:", selected_book["id"])
        print("Book Title:", selected_book["title"])
        print("Author:", selected_book["author"])
        print("Customer:", customer_name)
        print("Available Copies:", selected_book["available_copies"])
        print("=" * 45)

        confirmation = input(
            "Do you want to confirm this reservation? (yes/no): "
        ).strip().lower()

        confirmed = confirmation in {"yes", "y"}

    if not confirmed:
        return {
            "success": True,
            "created": False,
            "message": "Reservation cancelled by the customer."
        }

    books = load_json(BOOKS_FILE)
    reservations = load_json(RESERVATIONS_FILE)

    selected_book = next(
        (book for book in books if book["id"] == book_id),
        None
    )

    if selected_book is None or selected_book["available_copies"] <= 0:
        return {
            "success": False,
            "created": False,
            "message": "The book is no longer available."
        }

    selected_book["available_copies"] -= 1

    existing_numbers = []

    for item in reservations:
        reservation_id = item.get("reservation_id", "")
        if reservation_id.startswith("RES"):
            try:
                existing_numbers.append(int(reservation_id[3:]))
            except ValueError:
                pass

    next_number = max(existing_numbers, default=0) + 1
    reservation_id = f"RES{next_number:03d}"

    reservation = {
        "reservation_id": reservation_id,
        "book_id": selected_book["id"],
        "book_title": selected_book["title"],
        "customer_name": customer_name,
        "reservation_date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "status": "Confirmed"
    }

    reservations.append(reservation)

    save_json(BOOKS_FILE, books)
    save_json(RESERVATIONS_FILE, reservations)

    return {
        "success": True,
        "created": True,
        "message": "Book reserved successfully!",
        "reservation": reservation,
        "remaining_copies": selected_book["available_copies"]
    }
