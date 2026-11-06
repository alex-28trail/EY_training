
import re


# 1. Input validation
def validate_input(user_input):
    if not user_input or not user_input.strip():
        return False, "Please enter a question."

    if len(user_input) > 500:
        return False, "Your question is too long. Maximum limit is 500 characters."

    return True, "Valid input."


# 2. Guest count validation
def validate_guest_count(guests):
    if guests < 1 or guests > 20:
        return False, "Guest count must be between 1 and 20."

    return True, "Valid guest count."


# 3. PII detection
def detect_pii(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    phone_pattern = r'(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)'

    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)

    return {
        "emails": emails,
        "phone_numbers": phones
    }


# 4. PII redaction
def redact_pii(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    phone_pattern = r'(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)'

    text = re.sub(email_pattern, "[EMAIL REDACTED]", text)
    text = re.sub(phone_pattern, "[PHONE REDACTED]", text)

    return text


# 5. Context handling
def is_contextual_followup(text):

    followup_patterns = [
        r"^yes$",
        r"^no$",
        r"^\d+\s*(people|guests|persons)$",
        r"^make that .+$",
        r"^increase it to .+$",
        r"^decrease it to .+$",
        r"^what about .+$",
        r"^same restaurant$",
        r"^that restaurant$",
        r"^calculate it again$",
        r"^do that$",
        r"^same$"
    ]

    text = text.lower().strip()

    return any(
        re.match(pattern, text)
        for pattern in followup_patterns
    )


# 6. Domain restriction
def is_restaurant_related(text):

    allowed_keywords = [
        "restaurant", "restaurants", "food", "cuisine",
        "indian", "italian", "chinese", "japanese",
        "spice garden", "olive bistro", "dragon wok",
        "coastal curry", "sakura house",
        "price", "cost", "dining", "guest", "guests",
        "people", "seat", "seats", "reservation",
        "book", "booking", "menu", "meal", "table",
        "yes", "no", "increase", "decrease",
        "more", "less", "same", "that", "it",
        "change", "make", "calculate", "show",
        "how much", "what if"
    ]

    text = text.lower().strip()

    return any(keyword in text for keyword in allowed_keywords)


# 7. Output guardrail
def validate_output(response):

    if not response or not response.strip():
        return "I couldn't generate a response. Please try again."

    return redact_pii(response)


# 8. Guardrail testing
if __name__ == "__main__":

    print("\n--- INPUT VALIDATION ---")
    print(validate_input("Show me Indian restaurants."))

    print("\n--- GUEST VALIDATION ---")
    print(validate_guest_count(6))
    print(validate_guest_count(50))

    print("\n--- PII DETECTION ---")
    sample = "My email is john@example.com"
    print(detect_pii(sample))

    print("\n--- PII REDACTION ---")
    print(redact_pii(sample))

    print("\n--- CONTEXT HANDLING ---")
    print(is_contextual_followup("Make that 6 people"))
    print(is_contextual_followup("yes"))
    print(is_contextual_followup("What is the largest mammal?"))

    print("\n--- DOMAIN RESTRICTION ---")
    print(is_restaurant_related("Show me Indian restaurants"))
    print(is_restaurant_related("What is the largest mammal?"))
