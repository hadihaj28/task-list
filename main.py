##authr:hadi hajyhia
##id:326608965

from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()

# "מסד נתונים" בזיכרון
tasks = []
counter = 1


@app.get("/tasks")
def get_tasks(priority: Optional[int] = None):
    # סינון אופציונלי לפי עדיפות
    if priority is not None:
        if priority not in [1, 2, 3]:
            raise HTTPException(status_code=400, detail="Priority filter must be 1, 2, or 3")
        return [task for task in tasks if task["priority"] == priority]

    # ללא סינון - החזרת כל המשימות
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks")
def add_task(task: dict):
    global counter

    # שליפת העדיפות, אם לא הוזנה - ברירת המחדל היא 2
    priority = task.get("priority", 2)

    # בדיקת תקינות לערך העדיפות
    if type(priority) is not int or priority not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Priority must be an integer between 1 and 3")

    new_task = {
        "id": counter,
        "title": task.get("title"),
        "owner": task.get("owner"),
        "priority": priority
    }
    tasks.append(new_task)
    counter += 1
    return new_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")