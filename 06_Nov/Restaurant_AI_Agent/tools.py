
import json
from pathlib import Path
from langchain.tools import tool

RESTAURANT_FILE = Path(__file__).parent / "restaurants.json"


def load_restaurants():
    with open(RESTAURANT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@tool
def search_restaurants(keyword: str) -> str:
    """
    Search restaurants using cuisine type or restaurant name.
    Returns matching restaurants with prices and available seats.
    """

    restaurants = load_restaurants()
    keyword = keyword.strip().lower()

    if not keyword:
        return "Please provide a cuisine type or restaurant name."

    matches = []

    for restaurant in restaurants:
        if (
            keyword in restaurant["cuisine"].lower()
            or keyword in restaurant["name"].lower()
        ):
            matches.append(restaurant)

    if not matches:
        return f"No restaurants found for '{keyword}'."

    results = []

    for restaurant in matches:
        results.append(
            f"ID: {restaurant['id']}\n"
            f"Name: {restaurant['name']}\n"
            f"Cuisine: {restaurant['cuisine']}\n"
            f"Location: {restaurant['location']}\n"
            f"Price per person: ₹{restaurant['price_per_person']}\n"
            f"Available seats: {restaurant['available_seats']}"
        )

    return "\n\n".join(results)


@tool
def calculate_dining_cost(restaurant_id: str, guests: int) -> str:
    """
    Calculate estimated dining cost using restaurant ID and guest count.
    """

    restaurants = load_restaurants()

    if guests < 1 or guests > 20:
        return "Invalid guest count. Please enter between 1 and 20 guests."

    restaurant = next(
        (
            item for item in restaurants
            if item["id"].lower() == restaurant_id.strip().lower()
        ),
        None
    )

    if restaurant is None:
        return f"Restaurant with ID '{restaurant_id}' does not exist."

    if guests > restaurant["available_seats"]:
        return (
            f"Only {restaurant['available_seats']} seats are available "
            f"at {restaurant['name']}. Cannot accommodate {guests} guests."
        )

    total_cost = restaurant["price_per_person"] * guests

    return (
        f"Restaurant: {restaurant['name']}\n"
        f"Price per person: ₹{restaurant['price_per_person']}\n"
        f"Number of guests: {guests}\n"
        f"Estimated total dining cost: ₹{total_cost}"
    )


if __name__ == "__main__":
    print("Restaurant tools loaded successfully.")
    print("Available tools:")
    print(search_restaurants.name)
    print(calculate_dining_cost.name)
