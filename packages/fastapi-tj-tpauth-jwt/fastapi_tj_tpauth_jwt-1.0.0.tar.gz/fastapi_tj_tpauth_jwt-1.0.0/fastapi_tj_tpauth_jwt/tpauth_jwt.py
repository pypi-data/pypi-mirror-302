from datetime import timedelta
from typing import Annotated, Callable, TypeVar, Optional, Generic, Any

from fastapi import Body, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse
from tj_tpauth import TJTPAuth, TPAuthStatus, Error, TPAuthData

from fastapi_tj_tpauth_jwt.jwt_utils import create_jwt, get_payload


class LoginForm(BaseModel):
    username: str
    password: str


T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    data: Optional[T]
    msg: Optional[str]
    code: Optional[int] = status.HTTP_200_OK


class JWTResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class UnauthorizedResponse(BaseModel):
    detail: str


def _provide_unauthorized_response(tpauth_status: TPAuthStatus):
    return JSONResponse(
        content=BaseResponse(
            data=UnauthorizedResponse(
                detail=tpauth_status.error.name,
            ),
            code=status.HTTP_401_UNAUTHORIZED,
            msg="Unauthorized",
        ).model_dump(),
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"}
    )


def _provide_jwt_response(access_token: str, refresh_token: str, token_type: str):
    return JSONResponse(
        content=BaseResponse(
            data=JWTResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type=token_type,
            ),
            msg="Success"
        ).model_dump()
    )


class TPAuthJWT:
    def __init__(
            self,
            tp_auth: TJTPAuth,
            secret_key: str,
            refresh_secret_key: str,
            access_token_expires_in: timedelta,
            refresh_token_expires_in: timedelta,
            algorithm: str = 'HS256'
    ):
        self._tp_auth = tp_auth

        self._secret_key = secret_key
        self._refresh_secret_key = refresh_secret_key
        self._access_token_expires_in = access_token_expires_in
        self._refresh_token_expires_in = refresh_token_expires_in
        self._algorithm = algorithm

        self._mock_tpauth_status = TPAuthStatus(
            status=False,
            error=Error.UNAUTHORIZED
        )

        self._unauthorized_response_provider = _provide_unauthorized_response
        self._jwt_response_provider = _provide_jwt_response

    @property
    def unauthorized_response_provider(self):
        return self._unauthorized_response_provider

    @unauthorized_response_provider.setter
    def unauthorized_response_provider(self, provider: Callable[[Error], Any]):
        self._unauthorized_response_provider = provider

    @property
    def jwt_response_provider(self):
        return self._jwt_response_provider

    @jwt_response_provider.setter
    def jwt_response_provider(self, provider: Callable[[str, str, str], Any]):
        self._jwt_response_provider = provider

    def _create_jwt_token(
            self,
            payload: TPAuthData
    ):
        access_token = create_jwt(
            payload.__dict__,
            self._access_token_expires_in,
            self._secret_key,
            self._algorithm,
        )
        refresh_token = create_jwt(
            payload.__dict__,
            self._refresh_token_expires_in,
            self._refresh_secret_key,
            self._algorithm,
        )

        return access_token, refresh_token

    def provide_login_handler(self):
        async def _login(
                login_form: Annotated[LoginForm, Body()],
        ):
            tpauth_status = await self._tp_auth.aio_login(login_form.username, login_form.password)
            if not tpauth_status.status:
                return self._unauthorized_response_provider(tpauth_status)

            access_token, refresh_token = self._create_jwt_token(tpauth_status.data)

            return self._jwt_response_provider(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type='Bearer'
            )

        return _login

    def provide_refresh_token_handler(self):
        async def _refresh_token(
                token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer(auto_error=False))]
        ):

            if token is None:
                return self._unauthorized_response_provider(self._mock_tpauth_status)

            payload = get_payload(
                token=token.credentials,
                secret_key=self._refresh_secret_key,
                algorithm=self._algorithm,
            )

            if payload is None:
                return self._unauthorized_response_provider(self._mock_tpauth_status)
            del payload['exp']

            access_token, refresh_token = self._create_jwt_token(TPAuthData(**payload))

            return self._jwt_response_provider(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type='Bearer'
            )

        return _refresh_token

    def provide_require_jwt(self):
        async def _require_jwt(
                token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer(auto_error=False))]
        ):
            if token is None:
                return self._unauthorized_response_provider(self._mock_tpauth_status)

            payload = get_payload(
                token=token.credentials,
                secret_key=self._secret_key,
                algorithm=self._algorithm
            )

            if payload is None:
                return self._unauthorized_response_provider(self._mock_tpauth_status)

            del payload['exp']
            return TPAuthData(**payload)

        return _require_jwt
