import uuid

from fastapi import APIRouter, Cookie
from schemas.users import Creds, Reg
from services.users import user_service
from starlette.responses import JSONResponse, Response

router = APIRouter()


@router.post(
    "/users/reg",
    response_model=None,
)
def register_user(data: Reg):
    return user_service.register(data)


@router.post(
    "/users/auth",
    response_model=None,
)
def auth_user(data: Creds, response: Response):
    return user_service.authorization(data, response)