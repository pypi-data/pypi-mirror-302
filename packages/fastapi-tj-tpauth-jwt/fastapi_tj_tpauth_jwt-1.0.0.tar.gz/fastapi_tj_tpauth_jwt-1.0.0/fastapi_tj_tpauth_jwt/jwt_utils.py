from datetime import timedelta, datetime, timezone

import jwt
from jwt import InvalidTokenError


def create_jwt(
        data: dict, expires_delta: timedelta,
        secret_key: str, algorithm: str = 'HS256'
):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def get_payload(
        token: str,
        secret_key: str, algorithm: str = 'HS256'
):
    try:
        payload: dict = jwt.decode(token, secret_key,
                                   algorithms=[algorithm])
    except InvalidTokenError:
        return None
    return payload
