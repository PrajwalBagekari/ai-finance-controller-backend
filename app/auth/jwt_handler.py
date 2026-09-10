from datetime import datetime
from datetime import timedelta
from datetime import timezone

from jose import jwt

from app.core.config import settings


def create_access_token(data: dict) -> str:
    payload = data.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload["exp"] = expire

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )