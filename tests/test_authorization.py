import pytest
from fastapi import HTTPException

from app.dependencies import verify_resource_owner


def test_owner_can_access_resource():
    result = verify_resource_owner(
        user_id=4,
        current_user_id=4
    )

    assert result == 4


def test_different_user_cannot_access_resource():
    with pytest.raises(HTTPException) as exc_info:
        verify_resource_owner(
            user_id=1,
            current_user_id=4
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == (
        "You are not authorized to access this user's resource"
    )