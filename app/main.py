import logging

from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import create_access_token
from app.db.database import get_db
from app.db.models import User, Subject, Task
from app.dependencies import get_current_user_id, verify_resource_owner
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.task import TaskResponse
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.security import hash_password, verify_password
from app.services.study_tip_service import (
    StudyTipServiceError,
    get_study_tip
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("studysync")


app = FastAPI(
    title="StudySync API",
    description=(
        "Backend API for the StudySync student study and performance "
        "management platform. Provides user authentication, user "
        "management, task search and filtering, study tips, and "
        "consistent error handling."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    logger.warning(
        "client_error | method=%s | path=%s | status_code=%s | detail=%s",
        request.method,
        request.url.path,
        exc.status_code,
        exc.detail
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "status_code": exc.status_code,
                "message": str(exc.detail)
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    logger.warning(
        "validation_error | method=%s | path=%s | status_code=422",
        request.method,
        request.url.path
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "status_code": 422,
                "message": "Invalid request data",
                "details": exc.errors()
            }
        }
    )


@app.exception_handler(Exception)
async def unexpected_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        "unexpected_error | method=%s | path=%s | error_type=%s",
        request.method,
        request.url.path,
        type(exc).__name__
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "status_code": 500,
                "message": "An unexpected server error occurred"
            }
        }
    )


@app.get("/health")
async def health_check(
    db: AsyncSession = Depends(get_db)
):
    try:
        await db.execute(select(1))

        return {
            "status": "healthy",
            "message": "StudySync backend is running",
            "database": "connected"
        }

    except Exception:
        return {
            "status": "unhealthy",
            "message": "StudySync backend is running",
            "database": "unavailable"
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
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists"
        )

    password_hash = hash_password(user_data.password)

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=password_hash
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@app.post(
    "/auth/login",
    response_model=TokenResponse
)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == login_data.email)
    )

    user = result.scalar_one_or_none()

    if user is None or not verify_password(
        login_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get(
    "/users",
    response_model=list[UserResponse]
)
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User)
        .where(User.id == current_user_id)
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
    current_user_id: int = Depends(verify_resource_owner),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(
            User.id == user_id,
            User.id == current_user_id
        )
    )

    user = result.scalar_one_or_none()

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
    current_user_id: int = Depends(verify_resource_owner),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(
            User.id == user_id,
            User.id == current_user_id
        )
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    update_data = user_data.model_dump(exclude_unset=True)

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

    if "password" in update_data:
        update_data["password_hash"] = hash_password(
            update_data.pop("password")
        )

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
    current_user_id: int = Depends(verify_resource_owner),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(
            User.id == user_id,
            User.id == current_user_id
        )
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    await db.delete(user)
    await db.commit()

    return None


@app.get(
    "/tasks",
    response_model=list[TaskResponse]
)
async def list_tasks(
    search: str | None = Query(
        default=None,
        min_length=1
    ),
    task_status: str | None = Query(
        default=None,
        alias="status"
    ),
    subject_id: int | None = Query(
        default=None,
        ge=1
    ),
    skip: int = Query(
        default=0,
        ge=0
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100
    ),
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(Task)
        .join(Subject, Task.subject_id == Subject.id)
        .where(Subject.user_id == current_user_id)
    )

    if search:
        query = query.where(
            Task.title.ilike(f"%{search}%")
        )

    if task_status:
        query = query.where(
            Task.status == task_status
        )

    if subject_id:
        query = query.where(
            Task.subject_id == subject_id
        )

    query = (
        query
        .order_by(Task.id)
        .offset(skip)
        .limit(limit)
    )

    result = await db.execute(query)

    tasks = result.scalars().all()

    return tasks


@app.get("/study-tip")
async def study_tip():
    try:
        tip = await get_study_tip()

        return {
            "study_tip": tip
        }

    except StudyTipServiceError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error)
        ) from error