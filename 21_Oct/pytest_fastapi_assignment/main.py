from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    status: str

tasks = [
        Task(id=1, title="Prepare report", status="Pending"),
        Task(id=2, title="Review invoice", status="Completed"),
        Task(id=3, title="Update dashboard", status="Pending"),
    ]

@app.get("/tasks")
def get_task():
    return tasks

@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task.id== id:
            return task

    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task.model_dump())
    return {"message": "Task created successfully"}


@app.put("/tasks/{id}")
def update_task(id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id== id:
            tasks[index] = updated_task
            return updated_task

    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{id}")
def delete_task(id: int):
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
            return {"message": "Task deleted successfully"}

    raise HTTPException(status_code=404, detail="Task not found")
