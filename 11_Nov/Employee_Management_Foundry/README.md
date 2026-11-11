# Employee Leave Management Agent

## Project Overview
Employee Leave Management Agent using Azure AI Foundry and Redis.

## Technologies Used
- Python
- Microsoft Azure AI Foundry
- FastAPI
- Redis
- Docker
- Azure Identity

## Leave Policies

| Leave Type    | Annual Entitlement |
| Casual Leave  | 12 Days |
| Sick Leave    | 10 Days |
| Annual Leave  | 18 Days |

**Policy Rules:**
- Leave applications must be submitted at least 2 days in advance, except sick leave.
- All leave requests require manager approval.

## Project Structure

```text
Employee_Management_Foundary/
│
├── main.py
├── requirements.txt
├── .env
└── README.md
```

## Execution commands
Azure login: az login

Install dependencies: pip install -r requirements.txt

Redis Installation: docker run -d --name emp-redis -p 127.0.0.1:6379:6379 -v emp_redis_data:/data redis:7-alpine redis-server --appendonly yes                

Redis Connection and Inspection:  docker exec -it emp-redis redis-cli

Execution: python -m uvicorn main:app --reload


## Test URL
[//]: # (http://127.0.0.1:8000/docs?utm_source=chatgpt.com#/default/chat_chat_post)

