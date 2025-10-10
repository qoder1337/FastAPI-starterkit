from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from src.database import DBSessionDep_local
from src.database import User
from src.schemas.user import User as UserSchema, UserCreate, UserUpdate
from src.utils.app_logger import logmsg


user_route = APIRouter(prefix="/users", tags=["users"])


@user_route.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: DBSessionDep_local):
    """NEW User"""
    result = await db.execute(select(User).where(User.username == user.username))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    db_user = User(
        username=user.username,
        hashed_password=f"hashed_{user.password}",  # TODO: real Hashing
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    logmsg.info(f"new user created: {db_user.username}")
    return db_user


@user_route.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db: DBSessionDep_local):
    """GET User by ID"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User nicht gefunden"
        )
    return user


@user_route.get("/", response_model=list[UserSchema])
async def list_users(db: DBSessionDep_local, skip: int = 0, limit: int = 100):
    """Lists all Users"""
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


@user_route.patch("/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user_update: UserUpdate, db: DBSessionDep_local):
    """Updates a User (partial update)"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User nicht gefunden"
        )

    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = f"hashed_{update_data.pop('password')}"

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user


@user_route.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: DBSessionDep_local):
    """DELETE User"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    await db.delete(user)
    logmsg.info(f"new user deleted: {user.username}")
    await db.commit()
