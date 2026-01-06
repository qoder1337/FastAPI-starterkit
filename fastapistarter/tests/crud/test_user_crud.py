from src.crud import user as user_crud
from src.schemas.user import UserCreate, UserUpdate

# No explicit 'import pytest' needed here.
# The runner automatically discovers functions starting with 'test_'.


# CRUD TestsDB-Session
async def test_create_user(test_db_session):
    user_in = UserCreate(username="crud_test", password="password123")
    user = await user_crud.create_user(test_db_session, user_in)

    assert user.username == "crud_test"
    assert hasattr(user, "id")
    assert user.hashed_password == "hashed_password123"


async def test_get_user_by_username(test_db_session):
    await user_crud.create_user(
        test_db_session, UserCreate(username="unique", password="x")
    )

    user = await user_crud.get_user_by_username(test_db_session, "unique")
    assert user is not None
    assert user.username == "unique"


async def test_get_users_pagination(test_db_session):
    # Setup: create 3 Users
    for i in range(3):
        await user_crud.create_user(
            test_db_session, UserCreate(username=f"user_{i}", password="x")
        )

    # Testing Limit
    users = await user_crud.get_users(test_db_session, limit=2)
    assert len(users) == 2

    # Testing Skip
    users_skip = await user_crud.get_users(test_db_session, skip=1, limit=2)
    assert len(users_skip) == 2
    assert users_skip[0].username == "user_1"


async def test_update_user(test_db_session):
    user = await user_crud.create_user(
        test_db_session, UserCreate(username="old", password="old")
    )

    # Update with new Password
    update_data = UserUpdate(username="new", password="new")
    updated_user = await user_crud.update_user(test_db_session, user, update_data)

    assert updated_user.username == "new"
    assert updated_user.hashed_password == "hashed_new"


async def test_delete_user(test_db_session):
    user = await user_crud.create_user(
        test_db_session, UserCreate(username="delete_me", password="x")
    )

    await user_crud.delete_user(test_db_session, user)

    deleted_user = await user_crud.get_user(test_db_session, user.id)
    assert deleted_user is None
