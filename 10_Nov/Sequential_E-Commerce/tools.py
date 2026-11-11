
import json
from pathlib import Path

from agent_framework import tool


DATA_FILE = Path(__file__).parent / "products.json"


def load_products():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# Tool 1: Search products

@tool(approval_mode="never_require")
def search_products(query: str) -> str:
    """Search products by product name or category."""

    print(f"\n[TOOL CALLED] search_products: {query}")

    products = load_products()

    matches = [
        product for product in products
        if query.lower() in product["name"].lower()
        or query.lower() in product["category"].lower()
    ]

    if not matches:
        return json.dumps({
            "message": f"No products found matching '{query}'.",
            "products": []
        })

    results = []

    for product in matches:
        results.append({
            "product_id": product["id"],
            "product_name": product["name"],
            "category": product["category"],
            "price": product["price_inr"],
            "stock": product["stock"],
            "rating": product["rating"]
        })

    return json.dumps({
        "message": "Matching products found.",
        "products": results
    })


# Tool 2: Calculate order total

@tool(approval_mode="never_require")
def calculate_order_total(product_id: str, quantity: int) -> str:
    """Calculate order total and verify product stock."""

    print(
        f"\n[TOOL CALLED] calculate_order_total: "
        f"{product_id}, {quantity}"
    )

    if not isinstance(quantity, int) or isinstance(quantity, bool):
        return json.dumps({
            "status": "error",
            "message": "Quantity must be a whole number."
        })

    if quantity < 1:
        return json.dumps({
            "status": "error",
            "message": "Quantity must be at least 1."
        })

    products = load_products()

    for product in products:

        if product["id"].upper() == product_id.upper():

            if quantity > product["stock"]:
                return json.dumps({
                    "status": "error",
                    "product_id": product_id,
                    "requested_quantity": quantity,
                    "available_stock": product["stock"],
                    "message": "Insufficient stock."
                })

            total = product["price_inr"] * quantity

            return json.dumps({
                "status": "success",
                "product_id": product["id"],
                "product_name": product["name"],
                "quantity": quantity,
                "price_per_unit": product["price_inr"],
                "available_stock": product["stock"],
                "total_cost": total,
                "rating": product["rating"],
                "currency": "INR"
            })

    return json.dumps({
        "status": "error",
        "message": f"Product {product_id} not found."
    })
