
import asyncio

from dotenv import load_dotenv
from agent_framework import AgentResponse
from agent_framework.orchestrations import SequentialBuilder

from agents import create_agents


load_dotenv()


async def main():

    # Step 1: Create agents
    inventory_agent, pricing_agent, recommendation_agent = create_agents()

    # Step 2: Build sequential workflow
    workflow = SequentialBuilder(
        participants=[
            inventory_agent,
            pricing_agent,
            recommendation_agent
        ],
        output_from="all"
    ).build()

    # Step 3: Get customer request
    question = input("\nCustomer: ").strip()

    if not question:
        print("Please enter a valid request.")
        return

    # Step 4: Execute workflow asynchronously
    print("\nStarting E-commerce Multi-Agent Workflow...\n")

    result = await workflow.run(question)

    # Step 5: Display intermediate and final outputs
    print("\n========== WORKFLOW RESULTS ==========\n")

    for output in result.get_outputs():

        if isinstance(output, AgentResponse):

            for message in output.messages:

                print(
                    f"\n--- {message.author_name or 'Agent'} ---"
                )

                print(message.text)

    print("\n========== WORKFLOW COMPLETED ==========\n")


if __name__ == "__main__":
    asyncio.run(main())
