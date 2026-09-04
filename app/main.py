from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserResponse
from app.security import hash_password


app = FastAPI(
    title="StudySync API",
    description="AI-Powered Student Study & Performance Platform",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "StudySync backend is running"
    }


@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    # Check whether the email is already registered
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists"
        )

    # Hash the password before storing it
    password_hash = hash_password(user_data.password)

    # Create the database user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=password_hash
    )

    # Save the user
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user