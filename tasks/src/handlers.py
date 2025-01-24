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
    SearchTasksIn, TaskIn, TaskOut
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
    save_task(task_id, task_data, False)
    return task_data


@router.get("", response_model=List[TaskOut])
async def read_all_tasks():
    """ Retrieves all tasks """
    return get_all_tasks()


@router.post("/_search", response_model=List[TaskOut])
async def search_tasks(search: SearchTasksIn):
    """ Retrieves specific tasks """
    search_data = search.dict()
    tasks = get_all_tasks()
    filtered_tasks = []
    for task in tasks:
        if "title" in search_data:
            if not fullmatch(search_data["title"], task["title"]):
                continue
        if "content" in search_data:
            if not fullmatch(search_data["content"], task["content"]):
                continue
        if "completed" in search_data:
            if search_data["completed"] != task["completed"]:
                continue
        if "importance"in search_data:
            if task["importance"] not in search_data["importance"]:
                continue
        filtered_tasks.append(task)
    return filtered_tasks


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
    task_data["revision_id"] = existing_task["revision_id"] + 1
    save_task(task_id, task_data, True)
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
