
import pytest
from fastapi.testclient import TestClient

from main import app, tasks, Task

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_tasks():
    """Reset the task list before every test."""
    tasks.clear()
    tasks.extend([
        Task(id=1, title="Prepare report", status="Pending"),
        Task(id=2, title="Review invoice", status="Completed"),
        Task(id=3, title="Update dashboard", status="Pending"),
    ])


# 1. GET /tasks returns status code 200
def test_get_tasks_status_code():
    response = client.get("/tasks")
    assert response.status_code == 200

#
# 2. GET /tasks returns a list
def test_get_tasks_returns_list():
    response = client.get("/tasks")
    assert isinstance(response.json(), list)

#
# 3. GET /tasks/1 returns the correct task
def test_get_task_by_id():
    response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1

#
# # 4. GET a nonexistent task returns 404
def test_get_nonexistent_task():
    response = client.get("/tasks/999")

    assert response.status_code == 404
#
#
# # 5. POST /tasks creates a task
def test_create_task():
    response=client.post(
        "/tasks",
        json={
            "id": 4,
            "title": "Check server logs",
            "status": "Pending"
        }
    )


    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 4
    assert data["title"] == "Checking server logs"
    assert data["status"] == "Pending"




# # 6. POST with a missing required field returns validation error
def test_create_task_missing_field():
    invalid_task = {
        "id": 4,
        "title": "Check server logs",
        # Missing status
    }

    response = client.post("/tasks", json=invalid_task)

    assert response.status_code == 422

#
# # 7. PUT /tasks/2 updates the task
def test_update_task():
    # Prepare a state where the status needs to change.
    tasks[1] = Task(
        id=2,
        title="Review invoice",
        status="Pending",
    )

    updated_task = {
        "id": 2,
        "title": "Review invoice",
        "status": "Completed",
    }

    response = client.put("/tasks/2", json=updated_task)
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == 2
    assert data["status"] == "Completed"
#
#
# # 8. DELETE /tasks/3 deletes the task successfully
# def test_delete_task():
#     response = client.delete("/tasks/3")
#
#     assert response.status_code == 200
#     assert response.json()["message"] == "Task deleted successfully"
#
#
# # 9. Deleted task should return 404
# def test_deleted_task_returns_404():
#     client.delete("/tasks/3")
#
#     response = client.get("/tasks/3")
#
#     assert response.status_code == 404
#
#
# # 10. Duplicate task IDs are rejected
# def test_duplicate_task_id():
#     duplicate_task = {
#         "id": 1,
#         "title": "Duplicate task",
#         "status": "Pending",
#     }
#
#     response = client.post("/tasks", json=duplicate_task)
#
#     assert response.status_code == 409
#
#
# # 11. Updating a nonexistent task returns 404
# def test_update_nonexistent_task():
#     missing_task = {
#         "id": 999,
#         "title": "Missing task",
#         "status": "Pending",
#     }
#
#     response = client.put("/tasks/999", json=missing_task)
#
#     assert response.status_code == 404
