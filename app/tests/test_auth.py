import pytest
from fastapi import HTTPException
from app.methods.token import get_current_user, verify_token

@pytest.mark.asyncio
async def test_get_current_user_success(test_db, test_user, test_token):
    # Тест успешного получения текущего пользователя
    user = await get_current_user(test_token, test_db)
    assert user.email == test_user.email

@pytest.mark.asyncio
async def test_get_current_user_invalid_token(test_db):
    # Тест с неверным токеном
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user("invalid_token", test_db)
    assert exc_info.value.status_code == 401

@pytest.mark.asyncio
async def test_verify_token_success(test_token):
    # Тест успешной верификации токена
    email = verify_token(test_token)
    assert email == "test@example.com"

@pytest.mark.asyncio
async def test_verify_token_invalid():
    # Тест с неверным токеном
    with pytest.raises(HTTPException) as exc_info:
        verify_token("invalid_token")
    assert exc_info.value.status_code == 401 