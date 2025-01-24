from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Optional


class ImportanceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class NoteIn(BaseModel):
    title: str
    content: str
    completed: bool = False
    progress: float = 0.0
    deadline: Optional[datetime]


class SearchNotesIn(BaseModel):
    title: Optional[str] = ".*"
    content: Optional[str] = ".*"
    completed: Optional[bool] = False


class NoteOut(NoteIn):
    id: str  # The ID of the note will be its filename (the email in this case)
    revision_id: int
    importance: ImportanceLevel
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
