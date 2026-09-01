from datetime import date
from pydantic import BaseModel


class StudySessionCreate(BaseModel):
    subject_id: int
    duration_minutes: int
    session_date: date


class StudySessionResponse(BaseModel):
    id: int
    subject_id: int
    duration_minutes: int
    session_date: date