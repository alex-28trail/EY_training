
import os

from agent_framework import Agent
from agent_framework.openai import OpenAIChatCompletionClient

from tools import search_products, calculate_order_total


def create_agents():

    client = OpenAIChatCompletionClient(
        model=os.getenv(
            "OPENAI_CHAT_COMPLETION_MODEL",
            "openai/gpt-4o-mini"
        ),
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv(
            "OPENAI_BASE_URL",
            "https://openrouter.ai/api/v1"
        )
    )

    inventory_agent = Agent(
        client=client,
        name="InventoryAgent",
        instructions="""
        You are an Inventory Agent for an e-commerce store.

        Your responsibilities:
        1. Understand the customer's product requirements.
        2. Identify the requested product category and quantity.
        3. Use the search_products tool to find matching products.
        4. Return product IDs, names, prices, stock quantities,
           and ratings.
        5. Clearly identify products that are out of stock.
        6. Pass the inventory findings and original customer
           requirements to the next agent.

        Do not make the final recommendation.
        """,
        tools=[search_products]
    )

    pricing_agent = Agent(
        client=client,
        name="PricingAgent",
        instructions="""
        You are a Pricing Agent for an e-commerce store.

        Your responsibilities:
        1. Read the customer's original request and inventory results.
        2. Identify the requested quantity and total budget.
        3. Use calculate_order_total for each relevant product.
        4. Verify stock availability.
        5. Calculate the total cost for the requested quantity.
        6. Identify products that exceed the customer's budget.
        7. Pass valid pricing and stock information to the
           Recommendation Agent.

        Never approve a product with insufficient stock.
        Never approve a product that exceeds the total budget.
        Do not make the final recommendation.
        """,
        tools=[calculate_order_total]
    )

    recommendation_agent = Agent(
        client=client,
        name="RecommendationAgent",
        instructions="""
        You are a Recommendation Agent for an e-commerce store.

        Your responsibilities:
        1. Review the original customer request.
        2. Review the inventory and pricing results.
        3. Recommend only products that satisfy the requested
           quantity, stock availability, and total budget.
        4. Select the product with the highest customer rating.
        5. If ratings are equal, select the lower-priced product.
        6. Explain why the selected product is suitable.
        7. If no product satisfies the requirements, clearly
           explain that no suitable product is available.

        Never recommend an out-of-stock product or a product
        that exceeds the customer's total budget.
        Do not invent product information.
        """,
    )

    return (
        inventory_agent,
        pricing_agent,
        recommendation_agent
    )
