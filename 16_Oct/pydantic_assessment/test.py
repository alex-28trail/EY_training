import json
import logging
from typing import Literal

from pydantic import BaseModel, EmailStr, ValidationError, field_validator


# -----------------------------
# Logging Configuration
# -----------------------------
logging.basicConfig(
    filename="registration.log",
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)


# -----------------------------
# Pydantic Model
# -----------------------------
class Registration(BaseModel):
    registration_id: str
    name: str
    email: EmailStr
    age: int
    ticket_type: Literal["Standard", "Premium", "VIP"]
    amount: float

    @field_validator("age")
    @classmethod
    def validate_age(cls, value):
        if value < 18:
            raise ValueError("Age must be at least 18")
        return value

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError("Amount must be greater than 0")
        return value


# -----------------------------
# Variables
# -----------------------------
valid_registrations = []
total_records = 0
invalid_records = 0


# -----------------------------
# Load and Validate JSON
# -----------------------------
try:
    with open("registrations.json", "r") as file:
        registrations = json.load(file)

    total_records = len(registrations)

    for record in registrations:
        try:
            registration = Registration(**record)

            valid_registrations.append(registration)

            logging.info(
                f"Registration {registration.registration_id} validated successfully"
            )

            if registration.ticket_type == "VIP":
                logging.warning(
                    f"VIP registration detected: {registration.registration_id}"
                )

        except ValidationError as e:
            invalid_records += 1

            for error in e.errors():
                field = ".".join(str(x) for x in error["loc"])
                message = error["msg"]

                print(
                    f"Registration ID: {record.get('registration_id')} | "
                    f"Field: {field} | Error: {message}"
                )

                logging.error(
                    f"Registration {record.get('registration_id')} | "
                    f"Field: {field} | Error: {message}"
                )

except FileNotFoundError:
    print("Error: registrations.json file not found.")
    logging.error("registrations.json file not found.")

except json.JSONDecodeError:
    print("Error: Invalid JSON format.")
    logging.error("Invalid JSON format in registrations.json.")

except Exception as e:
    print(f"Unexpected Error: {e}")
    logging.error(str(e))


# -----------------------------
# Print Valid Registrations
# -----------------------------
print("\nValid Registrations:")
for reg in valid_registrations:
    print(reg)


# -----------------------------
# Serialize One Valid Object
# -----------------------------
if valid_registrations:
    first_valid = valid_registrations[0]

    print("\nDictionary Serialization:")
    print(first_valid.model_dump())

    print("\nJSON Serialization:")
    print(first_valid.model_dump_json(indent=4))


# -----------------------------
# Save Valid Registrations
# -----------------------------
try:
    with open("valid_registrations.json", "w") as file:
        json.dump(
            [reg.model_dump() for reg in valid_registrations],
            file,
            indent=4
        )
except Exception as e:
    print(f"Error saving valid registrations: {e}")
    logging.error(f"Error saving valid registrations: {e}")


# -----------------------------
# Summary
# -----------------------------
print("\nSummary")
print(f"Total records: {total_records}")
print(f"Valid records: {len(valid_registrations)}")
print(f"Invalid records: {invalid_records}")