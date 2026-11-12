
import asyncio
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Never

from dotenv import load_dotenv
from openai import AsyncOpenAI

from agent_framework import (
    Agent,
    Executor,
    WorkflowBuilder,
    WorkflowContext,
    executor,
    handler,
    response_handler,
)
from agent_framework.openai import OpenAIChatClient


# =====================================================
# 1. CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


def read_setting(name: str) -> str:
    value = os.getenv(name, "").strip()

    if (
        not value
        or value.startswith("PASTE_")
        or value.startswith("YOUR_")
    ):
        raise ValueError(
            f"Set {name} correctly in your .env file"
        )

    return value


# =====================================================
# 2. HUMAN APPROVAL REQUEST
# =====================================================

@dataclass
class ManagerApprovalRequest:
    return_request: dict
    prompt: str


# =====================================================
# 3. DETERMINISTIC ELIGIBILITY CHECKS
# =====================================================

def check_eligibility(return_request: dict) -> dict:

    findings = []
    issues = []

    amount = float(return_request["amount_inr"])
    days = int(return_request["days_since_delivery"])
    previous_returns = int(
        return_request["previous_returns_90_days"]
    )

    condition = (
        return_request["item_condition"]
        .strip()
        .upper()
    )

    invoice_available = return_request[
        "invoice_available"
    ]

    photo_available = return_request[
        "photo_evidence_available"
    ]

    # CONDITION 1: Amount below Rs. 25,000

    if amount < 25000:
        findings.append(
            "PASS: Product amount is below Rs. 25,000."
        )
    else:
        issues.append(
            "Product amount is Rs. 25,000 or above."
        )

    # CONDITION 2: Within 30 days

    if days <= 30:
        findings.append(
            "PASS: Return request is within 30 days."
        )
    else:
        issues.append(
            "Return request exceeds the 30-day period."
        )

    # CONDITION 3: Invoice available

    if invoice_available is True:
        findings.append(
            "PASS: Customer invoice is available."
        )
    else:
        issues.append(
            "Customer invoice is missing."
        )

    # CONDITION 4: Item condition

    if condition == "UNOPENED":
        findings.append(
            "PASS: Item is unopened."
        )

    elif condition == "DAMAGED" and photo_available is True:
        findings.append(
            "PASS: Damaged item has supporting photographs."
        )

    else:
        issues.append(
            "Item condition does not meet automatic "
            "approval requirements."
        )

    # CONDITION 5: Previous returns

    if previous_returns < 3:
        findings.append(
            "PASS: Fewer than three previous returns "
            "within 90 days."
        )
    else:
        issues.append(
            "Customer has three or more previous returns "
            "within 90 days."
        )

    eligible = len(issues) == 0

    return {
        "eligible": eligible,
        "eligibility_findings": findings,
        "eligibility_issues": issues,
    }


# =====================================================
# 4. HUMAN-IN-THE-LOOP APPROVAL GATEWAY
# =====================================================

class ApprovalGateway(Executor):

    def __init__(self):
        super().__init__(id="approval_gateway")

    @handler
    async def review(
        self,
        return_request: dict,
        ctx: WorkflowContext[dict],
    ) -> None:

        needs_approval = (
            not return_request["eligible"]
            or return_request["risk_level"] == "HIGH"
        )

        # ---------------------------------------------
        # AUTOMATIC APPROVAL
        # ---------------------------------------------

        if not needs_approval:

            return_request["approval_route"] = "Automatic"

            return_request["final_decision"] = (
                "AUTO_APPROVED"
            )

            return_request["decision_by"] = (
                "Automatic approval policy"
            )

            print(
                "\n[Approval Gateway] "
                "Automatically approved."
            )

            await ctx.send_message(return_request)

            return

        # ---------------------------------------------
        # HUMAN APPROVAL REQUIRED
        # ---------------------------------------------

        return_request["approval_route"] = "Human Review"

        print(
            "\n[Approval Gateway] "
            "PAUSED - Manager approval required."
        )

        prompt = (
            f"Request ID: {return_request['request_id']}\n"
            f"Order ID: {return_request['order_id']}\n"
            f"Product: {return_request['product']}\n"
            f"Amount: INR "
            f"{return_request['amount_inr']:,}\n"
            f"Eligibility Issues: "
            f"{return_request['eligibility_issues']}\n"
            f"Risk Assessment: "
            f"{return_request['risk_assessment']}"
        )

        await ctx.request_info(
            request_data=ManagerApprovalRequest(
                return_request=return_request,
                prompt=prompt,
            ),
            response_type=str,
        )

    # ---------------------------------------------
    # MANAGER RESPONSE HANDLER
    # ---------------------------------------------

    @response_handler
    async def on_manager_decision(
        self,
        original_request: ManagerApprovalRequest,
        response: str,
        ctx: WorkflowContext[dict],
    ) -> None:

        return_request = dict(
            original_request.return_request
        )

        decision = response.strip().lower()

        if decision not in {"approve", "reject"}:
            raise ValueError(
                "Invalid manager decision. "
                "Enter approve or reject."
            )

        if decision == "approve":

            return_request["final_decision"] = (
                "MANAGER_APPROVED"
            )

        else:

            return_request["final_decision"] = (
                "MANAGER_REJECTED"
            )

        return_request["decision_by"] = "Human manager"

        print(
            "\n[Approval Gateway] "
            f"Manager decision: {decision.upper()}"
        )

        # Resume workflow with preserved request context

        await ctx.send_message(return_request)


# =====================================================
# 5. BUILD MULTI-AGENT WORKFLOW
# =====================================================

def build_workflow(chat_client: OpenAIChatClient):

    # -------------------------------------------------
    # AGENT 1: ELIGIBILITY AGENT
    # -------------------------------------------------

    eligibility_agent = Agent(
        client=chat_client,
        name="EligibilityAgent",
        instructions=(
            "You are an e-commerce return eligibility "
            "specialist. "

            "Review customer return requests using "
            "the following company policy: "

            "1. Product amount must be below INR 25,000. "
            "2. Request must be within 30 days of delivery. "
            "3. Customer invoice must be available. "
            "4. Item must be unopened, or damaged with "
            "supporting photographs. "
            "5. Customer must have fewer than three "
            "previous returns within 90 days. "

            "Explain which conditions appear satisfied "
            "and identify exceptions. "

            "Do not make the final approval decision. "
            "Python business rules determine eligibility. "
            "Use only the supplied request information."
        ),
    )

    # -------------------------------------------------
    # AGENT 2: RISK AGENT
    # -------------------------------------------------

    risk_agent = Agent(
        client=chat_client,
        name="RiskAgent",
        instructions=(
            "You are an e-commerce return risk analyst. "

            "Assess the customer request for: "

            "1. High-value refund requests. "
            "2. Unusually frequent returns. "
            "3. Missing invoices. "
            "4. Missing photographs for damaged items. "
            "5. Other suspicious or exceptional details. "

            "Return HIGH if you identify a significant "
            "risk. Otherwise return LOW. "

            "Start your response with HIGH or LOW, "
            "followed by a short explanation. "

            "Do not make the final approval decision."
        ),
    )

    # -------------------------------------------------
    # AGENT 3: CUSTOMER RESPONSE AGENT
    # -------------------------------------------------

    customer_response_agent = Agent(
        client=chat_client,
        name="CustomerResponseAgent",
        instructions=(
            "You are an e-commerce customer support "
            "communication specialist. "

            "Generate a polite, professional customer "
            "message using the supplied final decision. "

            "If the decision is AUTO_APPROVED, communicate "
            "that the request has been approved under "
            "the automatic policy. "

            "If the decision is MANAGER_APPROVED, "
            "communicate that the manager has approved "
            "the request. "

            "If the decision is MANAGER_REJECTED, "
            "politely communicate that the request "
            "was rejected after human review. "

            "Mention the product and whether the customer "
            "requested a refund or replacement. "

            "Never override the supplied decision. "
            "Never claim that a refund has been processed "
            "or a replacement has been shipped. "

            "This is a simulation. Do not claim that "
            "any actual transaction has occurred."
        ),
    )

    # =================================================
    # EXECUTOR 1: ELIGIBILITY REVIEW
    # =================================================

    @executor(id="eligibility_review")
    async def eligibility_review(
        return_request: dict,
        ctx: WorkflowContext[dict],
    ) -> None:

        print(
            "\n[Eligibility Agent] "
            "Reviewing return request..."
        )

        result = await eligibility_agent.run(
            "Review this return request against "
            "the company return policy:\n"
            + json.dumps(
                return_request,
                ensure_ascii=False,
            )
        )

        # Deterministic Python policy evaluation

        eligibility_result = check_eligibility(
            return_request
        )

        updated_request = {
            **return_request,
            **eligibility_result,
            "eligibility_agent_review": result.text.strip(),
        }

        print(
            "[Eligibility Agent] "
            f"Eligible: {eligibility_result['eligible']}"
        )

        for issue in eligibility_result[
            "eligibility_issues"
        ]:
            print(f"  Issue: {issue}")

        await ctx.send_message(updated_request)

    # =================================================
    # EXECUTOR 2: RISK REVIEW
    # =================================================

    @executor(id="risk_review")
    async def risk_review(
        return_request: dict,
        ctx: WorkflowContext[dict],
    ) -> None:

        print(
            "\n[Risk Agent] "
            "Analyzing return request..."
        )

        result = await risk_agent.run(
            "Assess the risk of this return request. "
            "Start with HIGH or LOW:\n"
            + json.dumps(
                return_request,
                ensure_ascii=False,
            )
        )

        risk_response = (
            result.text.strip().upper()
        )

        first_word = (
            risk_response.split()[0]
            .strip("*:.,")
            if risk_response
            else ""
        )

        if first_word not in {"HIGH", "LOW"}:
            risk_level = "HIGH"
        else:
            risk_level = first_word

        # Deterministic risk safeguards

        if (
            return_request["amount_inr"] >= 25000
            or return_request["previous_returns_90_days"] >= 3
            or not return_request["invoice_available"]
            or (
                return_request["item_condition"].upper()
                == "DAMAGED"
                and not return_request["photo_evidence_available"]
            )
        ):
            risk_level = "HIGH"

        updated_request = {
            **return_request,
            "risk_level": risk_level,
            "risk_assessment": result.text.strip(),
        }

        print(
            f"[Risk Agent] Risk Level: {risk_level}"
        )

        await ctx.send_message(updated_request)

    # =================================================
    # EXECUTOR 3: CUSTOMER RESPONSE
    # =================================================

    @executor(id="customer_response")
    async def customer_response(
        return_request: dict,
        ctx: WorkflowContext[Never, str],
    ) -> None:

        print(
            "\n[Customer Response Agent] "
            "Preparing customer communication..."
        )

        result = await customer_response_agent.run(
            "Prepare the customer-facing communication "
            "for this final workflow decision:\n"
            + json.dumps(
                return_request,
                ensure_ascii=False,
            )
        )

        # Construct structured final response

        final_output = {
            "request_id": return_request["request_id"],
            "order_id": return_request["order_id"],
            "product": return_request["product"],
            "requested_amount_inr": (
                return_request["amount_inr"]
            ),
            "request_type": return_request["request_type"],
            "eligibility_findings": (
                return_request["eligibility_findings"]
            ),
            "eligibility_issues": (
                return_request["eligibility_issues"]
            ),
            "eligibility_agent_review": (
                return_request["eligibility_agent_review"]
            ),
            "risk_level": return_request["risk_level"],
            "risk_assessment": (
                return_request["risk_assessment"]
            ),
            "approval_route": return_request["approval_route"],
            "final_decision": return_request["final_decision"],
            "decision_by": return_request["decision_by"],
            "customer_communication": result.text.strip(),
        }

        print(
            "\n[Customer Response Agent] "
            "Final response generated."
        )

        await ctx.yield_output(
            json.dumps(
                final_output,
                ensure_ascii=False,
                indent=4,
            )
        )

    # =================================================
    # CREATE GRAPH WORKFLOW
    # =================================================

    gateway = ApprovalGateway()

    workflow = (
        WorkflowBuilder(
            start_executor=eligibility_review
        )
        .add_edge(
            eligibility_review,
            risk_review,
        )
        .add_edge(
            risk_review,
            gateway,
        )
        .add_edge(
            gateway,
            customer_response,
        )
        .build()
    )

    return workflow


# =====================================================
# 6. RUN WORKFLOW WITH HUMAN APPROVAL
# =====================================================

async def run_one(
    workflow,
    return_request: dict,
) -> None:

    responses = None
    first_run = True

    while True:

        # Initial execution or resumed execution

        if first_run:

            stream = workflow.run(
                return_request,
                stream=True,
            )

            first_run = False

        else:

            stream = workflow.run(
                stream=True,
                responses=responses,
            )

        pending = {}
        completed = False

        async for event in stream:

            if event.type == "request_info":

                pending[event.request_id] = event.data

            elif event.type == "output":

                print("\n" + "=" * 65)
                print("FINAL RETURN PROCESSING OUTPUT")
                print("=" * 65)

                print(event.data)

                print("=" * 65)

                completed = True

        if completed:
            return

        if not pending:

            raise RuntimeError(
                "Workflow stopped without final output "
                "or human approval request."
            )

        responses = {}

        # ---------------------------------------------
        # MANAGER INPUT
        # ---------------------------------------------

        for request_id, request in pending.items():

            print("\n" + "=" * 65)
            print("HUMAN-IN-THE-LOOP APPROVAL REQUIRED")
            print("=" * 65)

            print(request.prompt)

            print("\nEnter manager decision.")

            while True:

                answer = input(
                    "\nType approve or reject: "
                ).strip().lower()

                if answer in {"approve", "reject"}:
                    break

                print(
                    "Invalid input. "
                    "Please enter approve or reject."
                )

            responses[request_id] = answer


# =====================================================
# 7. MAIN APPLICATION
# =====================================================

async def main() -> None:

    print("=" * 65)
    print("MICROSOFT AGENT FRAMEWORK")
    print("E-COMMERCE RETURNS & REFUND PROCESSING")
    print("Authentication: Azure AI Foundry API Key")
    print("=" * 65)

    # ---------------------------------------------
    # LOAD AZURE FOUNDRY CONFIGURATION
    # ---------------------------------------------

    api_key = read_setting(
        "AZURE_OPENAI_API_KEY"
    )

    base_url = read_setting(
        "AZURE_OPENAI_BASE_URL"
    )

    deployment = read_setting(
        "AZURE_OPENAI_MODEL"
    )

    print("\nAzure Foundry configuration loaded.")
    print(f"Endpoint: {base_url}")
    print(f"Deployment: {deployment}")

    # ---------------------------------------------
    # LOAD RETURNS.JSON
    # ---------------------------------------------

    returns_file = BASE_DIR / "returns.json"

    if not returns_file.exists():

        raise FileNotFoundError(
            "returns.json was not found in the project folder."
        )

    with returns_file.open(
        encoding="utf-8"
    ) as file:

        return_requests = json.load(file)

    if not isinstance(return_requests, list):

        raise ValueError(
            "returns.json must contain a JSON list."
        )

    print(
        f"\nTotal return requests loaded: "
        f"{len(return_requests)}"
    )

    # ---------------------------------------------
    # CONNECT TO AZURE AI FOUNDRY
    # ---------------------------------------------

    async with AsyncOpenAI(
        api_key=api_key,
        base_url=base_url,
    ) as sdk_client:

        chat_client = OpenAIChatClient(
            model=deployment,
            async_client=sdk_client,
        )

        print(
            "\nAzure Foundry client initialized."
        )

        # -----------------------------------------
        # PROCESS EACH RETURN REQUEST
        # -----------------------------------------

        for return_request in return_requests:

            print("\n" + "=" * 65)

            print(
                f"Processing Request: "
                f"{return_request['request_id']}"
            )

            print(
                f"Order ID: {return_request['order_id']}"
            )

            print(
                f"Product: {return_request['product']}"
            )

            print(
                f"Amount: INR "
                f"{return_request['amount_inr']:,}"
            )

            print("=" * 65)

            # Create a fresh workflow for each request

            workflow = build_workflow(chat_client)

            await run_one(
                workflow,
                return_request,
            )

        print("\n" + "=" * 65)
        print("ALL RETURN REQUESTS PROCESSED")
        print("=" * 65)


# =====================================================
# 8. APPLICATION ENTRY POINT
# =====================================================

if __name__ == "__main__":

    try:
        asyncio.run(main())

    except ValueError as error:

        print(f"\nConfiguration/Input Error: {error}")

    except FileNotFoundError as error:

        print(f"\nFile Error: {error}")

    except Exception as error:

        print(
            f"\nApplication Error: "
            f"{type(error).__name__}: {error}"
        )
        raise
