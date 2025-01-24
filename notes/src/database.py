from datetime import datetime
import json
from pathlib import Path

from settings import settings


# Directory containing notes JSON files
DATA_DIRECTORY = Path(settings.DATA_DIRECTORY)
if not DATA_DIRECTORY.exists():
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)


def _get_note_path(note_id) -> Path:
    """ Returns the path of the file corresponding to a note """
    return Path(DATA_DIRECTORY) / f"{note_id}.json"


def get_all_notes():
    """ Retrieves all notes stored in JSON files """
    # Path(DATA_DIRECTORY) points to the directory containing the notes
    notes_directory = Path(DATA_DIRECTORY)

    # We go through all the JSON files in this directory
    notes = []
    for note_file in notes_directory.glob("*.json"):
        # For each file, load it and add its content to the list of notes
        with note_file.open("r", encoding="utf-8") as f:
            note_data = json.load(f)
            notes.append(note_data)

    return notes


def get_note(note_id):
    note_file_path = _get_note_path(note_id)

    if not note_file_path.is_file():
        return None
    with note_file_path.open("r", encoding="utf-8") as f:
        note_data = json.load(f)

    return note_data


def save_note(note_id, note_data, update_flag):
    note_file = _get_note_path(note_id)
    if update_flag:
        note_data["updated_at"] = str(datetime.now())
    else:
        note_data["created_at"] = str(datetime.now())
    note_data["deadline"] = str(note_data["deadline"])
    with open(note_file, "w", encoding="utf-8") as f:
        json.dump(note_data, f, indent=4, ensure_ascii=False)


def delete_note(note_id):
    """ Deletes a note by removing its corresponding file """
    note_file_path = _get_note_path(note_id)

    # Check if the file exists
    if note_file_path.is_file():
        # If the file exists, delete it
        note_file_path.unlink()
        return True
    else:
        # If the file does not exist, return False
        return False


def delete_all_notes():
    """ Delete all notes stored in JSON files """
    # Path(DATA_DIRECTORY) points to the directory containing the notes
    notes_directory = Path(DATA_DIRECTORY)

    # We go through all the JSON files in this directory
    for note_file in notes_directory.glob("*.json"):
        # For each file, delete it
        note_file.unlink()
