from fastapi import APIRouter
from api_fuctions.users import *
from starlette.responses import Response

router = APIRouter()


@router.post(
    "/users/reg",
    response_model=None,
)
def register_user(data: Reg):
    return register(data)


@router.post(
    "/users/auth",
    response_model=None,
)
def auth_user(data: Creds, response: Response):
    return authorization(data, response)
