from app.schemas.user import UserCreate
from app.schemas.subject import SubjectCreate
from app.schemas.task import TaskCreate
from app.schemas.performance import PerformanceCreate
from app.schemas.study_session import StudySessionCreate


user = UserCreate(
    name="Fowmiya",
    email="fowmiya@example.com",
    password="testpassword"
)

print("User:", user)


subject = SubjectCreate(
    name="Machine Learning",
    description="Study ML concepts"
)

print("Subject:", subject)


task = TaskCreate(
    title="Revise Linear Regression",
    subject_id=1
)

print("Task:", task)


performance = PerformanceCreate(
    subject_id=1,
    score=82,
    max_score=100,
    exam_type="Internal"
)

print("Performance:", performance)


study_session = StudySessionCreate(
    subject_id=1,
    duration_minutes=90,
    session_date="2026-09-01"
)

print("Study Session:", study_session)