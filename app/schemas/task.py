from datetime import date
from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    due_date: date | None = None
    status: str = "pending"
    subject_id: int


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    due_date: date | None
    status: str
    subject_id: int