from copy import copy
import json
from pathlib import Path

from settings import settings


# Directory containing tasks JSON files
DATA_DIRECTORY = Path(settings.DATA_DIRECTORY)
if not DATA_DIRECTORY.exists():
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)


def _get_task_path(task_id) -> Path:
    """ Returns the path of the file corresponding to a task """
    return Path(DATA_DIRECTORY) / f"{task_id}.json"


def get_all_tasks():
    """ Retrieves all tasks stored in JSON files """
    # Path(DATA_DIRECTORY) points to the directory containing the tasks
    tasks_directory = Path(DATA_DIRECTORY)

    # We go through all the JSON files in this directory
    tasks = []
    for task_file in tasks_directory.glob("*.json"):
        # For each file, load it and add its content to the list of tasks
        with task_file.open("r", encoding="utf-8") as f:
            task_data = json.load(f)
            tasks.append(task_data)

    return tasks


def get_task(task_id):
    task_file_path = _get_task_path(task_id)

    if not task_file_path.is_file():
        return None
    with task_file_path.open("r", encoding="utf-8") as f:
        task_data = json.load(f)

    return task_data


def save_task(task_id, task_data):
    task_clone = copy(task_data)
    task_file = _get_task_path(task_id)
    if "deadline" in task_clone and task_clone["deadline"]:
        task_clone["deadline"] = str(task_clone["deadline"])
    else:
        task_clone.pop("deadline", None)
    if "created_at" in task_clone and task_clone["created_at"]:
        task_clone["created_at"] = str(task_clone["created_at"])
    else:
        task_clone.pop("created_at", None)
    if "updated_at" in task_clone and task_clone["updated_at"]:
        task_clone["updated_at"] = str(task_clone["updated_at"])
    else:
        task_clone.pop("updated_at", None)
    with open(task_file, "w", encoding="utf-8") as f:
        json.dump(task_clone, f, indent=4, ensure_ascii=False)


def delete_task(task_id):
    """ Deletes a task by removing its corresponding file """
    task_file_path = _get_task_path(task_id)

    # Check if the file exists
    if task_file_path.is_file():
        # If the file exists, delete it
        task_file_path.unlink()
        return True
    else:
        # If the file does not exist, return False
        return False


def delete_all_tasks():
    """ Delete all tasks stored in JSON files """
    # Path(DATA_DIRECTORY) points to the directory containing the tasks
    tasks_directory = Path(DATA_DIRECTORY)

    # We go through all the JSON files in this directory
    for task_file in tasks_directory.glob("*.json"):
        # For each file, delete it
        task_file.unlink()
