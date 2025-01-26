from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class ImportanceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class TaskIn(BaseModel):
    title: str
    content: str
    completed: bool = False
    progress: float = 0.0
    deadline: Optional[datetime]


class SearchTasksIn(BaseModel):
    title: Optional[str] = ".*"
    content: Optional[str] = ".*"
    completed: Optional[bool] = False
    importance: Optional[List[ImportanceLevel]] = [ImportanceLevel.LOW, ImportanceLevel.MEDIUM]


class TaskOut(TaskIn):
    id: str  # The ID of the task will be its filename (the email in this case)
    revision_id: int
    importance: ImportanceLevel
    created_at: datetime
    updated_at: Optional[datetime] = None


class Metadata(BaseModel):
    selected: int
    total: int


class ListTaskOut(BaseModel):
    data: List[TaskOut]
    metadata: Metadata
