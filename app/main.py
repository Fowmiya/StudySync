from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
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


@app.get(
    "/users",
    response_model=list[UserResponse]
)
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    # Fetch users with stable ordering by ID
    result = await db.execute(
        select(User)
        .order_by(User.id)
        .offset(skip)
        .limit(limit)
    )

    users = result.scalars().all()

    return users


@app.get(
    "/users/{user_id}",
    response_model=UserResponse
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    # Find the user by their ID
    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    # Return 404 if the user does not exist
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@app.patch(
    "/users/{user_id}",
    response_model=UserResponse
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    # Find the user to update
    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    # Return 404 if the user does not exist
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get only the fields that were actually provided
    update_data = user_data.model_dump(exclude_unset=True)

    # Check for duplicate email before updating
    if "email" in update_data:
        result = await db.execute(
            select(User).where(
                User.email == update_data["email"],
                User.id != user_id
            )
        )

        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists"
            )

    # Hash the password if it is being updated
    if "password" in update_data:
        update_data["password_hash"] = hash_password(
            update_data.pop("password")
        )

    # Apply the provided changes
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    return user


@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    # Find the user to delete
    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    # Return 404 if the user does not exist
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Delete the user
    await db.delete(user)
    await db.commit()

    return None