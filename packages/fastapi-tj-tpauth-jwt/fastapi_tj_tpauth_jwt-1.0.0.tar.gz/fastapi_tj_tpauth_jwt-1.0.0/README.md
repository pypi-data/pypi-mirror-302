# fastapi-tj-tpauth-jwt

![PyPI - Version](https://img.shields.io/pypi/v/fastapi-tj-tpauth-jwt)

Integrate JWT into FastAPI using TP Servers authentication.

## Installation

```bash
pip install fastapi-tj-tpauth-jwt
```

## Usage

### Basic Example

```python
from datetime import timedelta
from typing import Annotated

from fastapi import FastAPI, Depends
from tj_tpauth import TJTPAuth, TPAuthData

from fastapi_tj_tpauth_jwt.tpauth_jwt import TPAuthJWT

app = FastAPI()

tpauth = TJTPAuth(
    host="localhost:8080"
)

tpauth_jwt = TPAuthJWT(
    tp_auth=tpauth,
    secret_key="<SECRET_KEY>",
    refresh_secret_key="<SECRET_KEY>",
    access_token_expires_in=timedelta(minutes=60),
    refresh_token_expires_in=timedelta(minutes=120),
    algorithm='HS256'
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/login")
async def login(
        login_res: Annotated[
            tpauth_jwt.provide_login_handler(), Depends()
        ]
):
    return login_res


@app.post("/refresh")
async def refresh(
        refresh_res: Annotated[
            tpauth_jwt.provide_refresh_token_handler(), Depends()
        ]
):
    return refresh_res


@app.get("/secret_data")
async def secret_data(
        payload: Annotated[
            tpauth_jwt.provide_require_jwt(), Depends()
        ]
):
    if not isinstance(payload, TPAuthData):
        return payload

    payload: TPAuthData

    return {
        "payload": payload.id,
    }

```

### Custom Unauthorized Error Response

```python
def unauthorized_response_provider(tpauth_status: TPAuthStatus):
    return {
        "error": "Unauthorized",
        "status": tpauth_status.error.value
    }


tpauth_jwt.unauthorized_response_provider = unauthorized_response_provider
```

### Custom JWT Response

```python
def jwt_provider(access_token: str, refresh_token: str, token_type: str):
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": token_type
    }


tpauth_jwt.jwt_response_provider = jwt_provider
```

## License

This library is released under the MIT License.

## Contact

If you have any questions or issues, please open an issue
on [GitHub](https://github.com/duynguyen02/fastapi-tj-tpauth-jwt/issues) or
email us at [duynguyen02.dev@gmail.com](mailto:duynguyen02.dev@gmail.com).