from fastapi import APIRouter, HTTPException, status
from re import fullmatch
from typing import List
from uuid import uuid4

from database import (
    get_note,
    get_all_notes,
    save_note,
    delete_note,
    delete_all_notes
)
from models import (
    ImportanceLevel,
    SearchNotesIn, NoteIn, NoteOut
)


router = APIRouter(
    prefix="/api/v1/notes",
    tags=["Notes"]
)


@router.post("", response_model=NoteOut,
             status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteIn,
                      importance: ImportanceLevel = ImportanceLevel.MEDIUM):
    """ Creates a new note and saves it """
    note_id = str(uuid4())
    note_data = note.dict()
    note_data["id"] = note_id
    note_data["importance"] = importance.value
    note_data["revision_id"] = 1
    save_note(note_id, note_data, False)
    return note_data


@router.get("", response_model=List[NoteOut])
async def read_all_notes():
    """ Retrieves all notes """
    return get_all_notes()


@router.post("/_search", response_model=List[NoteOut])
async def search_notes(search: SearchNotesIn):
    """ Retrieves specific notes """
    search_data = search.dict()
    notes = get_all_notes()
    filtered_notes = []
    for note in notes:
        if "title" in search_data:
            if not fullmatch(search_data["title"], note["title"]):
                continue
        if "content" in search_data:
            if not fullmatch(search_data["content"], note["content"]):
                continue
        if "completed" in search_data:
            if search_data["completed"] != note["completed"]:
                continue
        filtered_notes.append(note)
    return filtered_notes
    


@router.get("/{note_id}", response_model=NoteOut)
async def read_note(note_id: str):
    """ Retrieves a specific note """
    note = get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=NoteOut)
async def update_note(note_id: str, note: NoteIn):
    """ Updates an existing note """
    existing_note = get_note(note_id)
    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found")    
    note_data = note.dict()
    note_data["id"] = note_id
    note_data["importance"] = existing_note["importance"]
    note_data["created_at"] = existing_note["created_at"]
    note_data["revision_id"] = existing_note["revision_id"] + 1
    save_note(note_id, note_data, True)
    return note_data


@router.delete("/{note_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_note_by_id(note_id: str):
    """ Deletes a specific note """
    if delete_note(note_id):
        return
    raise HTTPException(status_code=404, detail="Note not found")


@router.delete("",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_notes_endpoint():
    """ Deletes all notes """
    delete_all_notes()
