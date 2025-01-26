import json
from pathlib import Path

from settings import DATA_DIRECTORY_PATH


# Directory containing users JSON files
DATA_DIRECTORY = Path(DATA_DIRECTORY_PATH)
if not DATA_DIRECTORY.exists():
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)


def __get_user_path(email) -> Path:
    """Returns the path of the file corresponding to a user"""
    return Path(DATA_DIRECTORY) / f"{email}.json"


def get_user(email):
    """Retrieve a user from a JSON file"""
    user_file_path = __get_user_path(email)
    if not user_file_path.is_file():
        return None
    with user_file_path.open("r", encoding="utf-8") as f:
        user_data = json.load(f)
    return user_data
