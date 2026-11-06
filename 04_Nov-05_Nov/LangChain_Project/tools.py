
import json
from pathlib import Path
from langchain.tools import tool

FILE = Path(__file__).parent / "workshops.json"
COUPON_FILE = Path(__file__).parent / "coupons.json"


def get_workshops():
    return json.loads(FILE.read_text(encoding="utf-8"))


def get_coupons():
    data = json.loads(COUPON_FILE.read_text(encoding="utf-8"))
    return data["coupons"]


@tool
def search_workshops(keyword: str) -> str:
    """Search available workshops by title."""

    matches = [
        w for w in get_workshops()
        if keyword.lower() in w["title"].lower()
    ]

    return json.dumps(matches)


@tool
def list_all_workshops() -> str:
    """List all available workshops with their IDs, titles and fees."""

    workshops = get_workshops()

    if not workshops:
        return "No workshops are currently available."

    return json.dumps(workshops, indent=4)


@tool
def find_cheapest_workshop() -> str:
    """Find and return the cheapest available workshop."""

    workshops = get_workshops()

    if not workshops:
        return "No workshops are currently available."

    cheapest = min(workshops, key=lambda w: w["fee"])

    return json.dumps({
        "workshop_id": cheapest["id"],
        "workshop": cheapest["title"],
        "fee": cheapest["fee"]
    }, indent=4)


@tool
def calculate_workshop_fee(
    workshop_id: str,
    participants: int,
    coupon_code: str = ""
) -> str:
    """Calculate workshop fees and optionally apply a valid coupon discount."""

    if participants < 1 or participants > 30:
        return "Participant count must be between 1 and 30."

    for workshop in get_workshops():

        if str(workshop["id"]) == str(workshop_id):

            original_total = workshop["fee"] * participants

            discount_percentage = 0
            discount_amount = 0
            final_total = original_total
            coupon_status = "No coupon applied."

            if coupon_code:

                coupon_code = coupon_code.strip().upper()

                for coupon in get_coupons():

                    if coupon["code"].upper() == coupon_code:

                        if coupon["active"]:

                            discount_percentage = coupon["discount"]

                            discount_amount = (
                                original_total * discount_percentage / 100
                            )

                            final_total = original_total - discount_amount

                            coupon_status = "Coupon applied successfully."

                        else:
                            coupon_status = "Coupon is inactive."

                        break

                else:
                    coupon_status = "Invalid coupon code."

            return json.dumps({
                "workshop": workshop["title"],
                "participants": participants,
                "original_total": original_total,
                "coupon_code": coupon_code if coupon_code else None,
                "coupon_status": coupon_status,
                "discount_percentage": discount_percentage,
                "discount_amount": discount_amount,
                "final_total": final_total
            }, indent=4)

    return "Workshop not found."


if __name__ == "__main__":

    print(list_all_workshops.invoke({}))

    print(find_cheapest_workshop.invoke({}))

    print(search_workshops.invoke({"keyword": "Python"}))

    print(calculate_workshop_fee.invoke({
        "workshop_id": "W101",
        "participants": 4,
        "coupon_code": "SAVE10"
    }))
