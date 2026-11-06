
import os
import re
import uuid

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

from tools import search_restaurants, calculate_dining_cost

from guardrails import (
    validate_input,
    detect_pii,
    redact_pii,
    is_restaurant_related,
    is_contextual_followup,
    validate_output
)
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = os.getenv("OPENAI_MODEL", "openai/gpt-4o-mini")

if not API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY not found. Check your .env file."
    )


# 1. Initialize GPT model through OpenRouter
model = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0,
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


# 2. Register Python tools
tools = [
    search_restaurants,
    calculate_dining_cost
]


# 3. System prompt
SYSTEM_PROMPT = """
You are a helpful AI Restaurant Reservation Assistant.

Your responsibilities:
1. Help users search available restaurants.
2. Help users calculate estimated dining costs.
3. Remember previously selected restaurants.
4. Remember the previous number of guests.
5. Handle follow-up questions using conversation history.

IMPORTANT RULES:

- Only answer restaurant-related questions.
- Use the registered Python tools for restaurant information
  and dining cost calculations.
- Never invent restaurant names.
- Never invent restaurant prices.
- Never invent available seats.
- Only provide restaurant information returned by the tools.
- When a user says "make that 6 people", use the
  previously selected restaurant.
- When a user asks about a previous calculation,
  use conversation history.
- If the restaurant is not known, ask the user to
  select a restaurant first.
- Do not make actual reservations.
- Do not process payments.
- Never claim a reservation has been booked.
- Clearly identify estimated dining costs.
- Guest count must be between 1 and 20.
- Respect the restaurant's available seat count.
- Be friendly and concise.
"""


# 4. Initialize conversation memory
memory = InMemorySaver()


# 5. Create LangChain agent
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=memory
)


# 6. Generate conversation ID
thread_id = str(uuid.uuid4())


def extract_guest_count(text):
    match = re.search(
        r"\b(\d+)\s*(?:guests?|people|persons?)\b",
        text,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    return None


def print_tool_calls(messages):
    for message in messages:
        if hasattr(message, "tool_calls"):
            for tool_call in message.tool_calls:
                print("\n[TOOL EXECUTION]")
                print("Tool Name:", tool_call["name"])
                print("Arguments:", tool_call["args"])


def get_response_content(content):
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        return "\n".join(
            item["text"]
            for item in content
            if isinstance(item, dict) and "text" in item
        )

    return str(content)


# 7. Main application
def main():

    global thread_id

    print("\n======================================")
    print("     RESTAURANT AI ASSISTANT")
    print("======================================")
    print("Provider: OpenRouter")
    print("Model:", MODEL_NAME)
    print("Type /new to start a fresh conversation.")
    print("Type exit to close the application.")

    while True:

        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            print("\nThank you for using Restaurant AI Assistant!")
            break

        # Reset conversation memory
        if user_input.lower() == "/new":
            thread_id = str(uuid.uuid4())
            print("\nNew conversation started.")
            print("Previous conversation memory has been reset.")
            continue

        # Input validation
        valid, message = validate_input(user_input)

        if not valid:
            print("\nGuardrail:", message)
            continue

        # PII detection and redaction
        pii = detect_pii(user_input)

        if pii["emails"] or pii["phone_numbers"]:

            print("\n[PII DETECTED]")
            print("Emails:", pii["emails"])
            print("Phone numbers:", pii["phone_numbers"])

            user_input = redact_pii(user_input)

            print("Redacted Input:", user_input)

        # Domain restriction
        if not is_restaurant_related(user_input) and not is_contextual_followup(user_input):

            if pii["emails"] or pii["phone_numbers"]:
                print(
                    "\nAssistant: Your personal information was "
                    "detected and redacted. I can only help with "
                    "restaurant-related questions."
                )
            else:
                print(
                    "\nGuardrail: I can only answer "
                    "restaurant-related questions."
                )

            continue

        # Guest count validation
        guests = extract_guest_count(user_input)

        if guests is not None and (guests < 1 or guests > 20):
            print(
                "\nGuardrail: Guest count must be between "
                "1 and 20. Please enter a valid number."
            )
            continue

        # Execute agent
        try:

            config = {
                "configurable": {
                    "thread_id": thread_id
                }
            }

            result = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": user_input
                        }
                    ]
                },
                config=config
            )

            # Display tool execution
            print_tool_calls(result["messages"])

            # Extract final response
            final_message = result["messages"][-1].content

            response = get_response_content(final_message)

            # Apply output guardrail
            response = validate_output(response)

            print("\nAssistant:", response)

        except Exception as error:
            print("\nApplication Error:", error)
            print("Check your OpenRouter API key, model and connection.")


if __name__ == "__main__":
    main()
