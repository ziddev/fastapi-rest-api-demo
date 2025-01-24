from datetime import datetime
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


def save_task(task_id, task_data, update_flag):
    task_file = _get_task_path(task_id)
    if update_flag:
        task_data["updated_at"] = str(datetime.now())
    else:
        task_data["created_at"] = str(datetime.now())
    task_data["deadline"] = str(task_data["deadline"])
    with open(task_file, "w", encoding="utf-8") as f:
        json.dump(task_data, f, indent=4, ensure_ascii=False)


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
