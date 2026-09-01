from pydantic import BaseModel


class PerformanceCreate(BaseModel):
    subject_id: int
    score: float
    max_score: float
    exam_type: str


class PerformanceResponse(BaseModel):
    id: int
    subject_id: int
    score: float
    max_score: float
    exam_type: str