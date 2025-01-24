from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from re import fullmatch
from typing import List
from uuid import uuid4

from database import (
    get_task,
    get_all_tasks,
    save_task,
    delete_task,
    delete_all_tasks
)
from models import (
    ImportanceLevel,
    SearchTasksIn, TaskIn,
    ListTaskOut, TaskOut
)


router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"]
)


@router.post("", response_model=TaskOut,
             status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskIn,
                      importance: ImportanceLevel = ImportanceLevel.MEDIUM):
    """ Creates a new task and saves it """
    task_id = str(uuid4())
    task_data = task.dict()
    task_data["id"] = task_id
    task_data["importance"] = importance.value
    task_data["revision_id"] = 1
    task_data["created_at"] = datetime.now()
    save_task(task_id, task_data)
    return task_data


@router.get("", response_model=List[TaskOut])
async def read_all_tasks():
    """ Retrieves all tasks """
    return get_all_tasks()


@router.post("/_search", response_model=ListTaskOut)
async def search_tasks(search: SearchTasksIn, selected: int = 10):
    """ Retrieves specific tasks """
    search_data = search.dict()
    tasks = get_all_tasks()
    filtered_tasks = []
    count = 0

    for task in tasks:
        if search_data["title"] and not fullmatch(search_data["title"], task["title"]):
            continue
        if search_data["content"] and not fullmatch(search_data["content"], task["content"]):
            continue
        if "completed" in search_data and search_data["completed"] != task["completed"]:
            continue
        if "importance" in search_data and task["importance"] not in search_data["importance"]:
            continue

        filtered_tasks.append(TaskOut(
            id=task["id"],
            revision_id=task["revision_id"],
            title=task["title"],
            content=task["content"],
            completed=task["completed"],
            progress=task["progress"],
            deadline=task.get("deadline"),
            importance=task["importance"],
            created_at=task["created_at"],
            updated_at=task.get("updated_at")
        ))
        count += 1
        if count >= selected:
            break

    return {"metadata": {"selected": count,
                         "total": len(tasks)},
            "data": filtered_tasks}


@router.get("/{task_id}", response_model=TaskOut)
async def read_task(task_id: str):
    """ Retrieves a specific task """
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskOut)
async def update_task(task_id: str, task: TaskIn):
    """ Updates an existing task """
    existing_task = get_task(task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task.dict()
    task_data["id"] = task_id
    task_data["importance"] = existing_task["importance"]
    task_data["created_at"] = existing_task["created_at"]
    task_data["updated_at"] = datetime.now()
    task_data["revision_id"] = existing_task["revision_id"] + 1
    save_task(task_id, task_data)
    return task_data


@router.delete("/{task_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_by_id(task_id: str):
    """ Deletes a specific task """
    if delete_task(task_id):
        return
    raise HTTPException(status_code=404, detail="Task not found")


@router.delete("",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_tasks_endpoint():
    """ Deletes all tasks """
    delete_all_tasks()
