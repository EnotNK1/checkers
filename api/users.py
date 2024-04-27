from fastapi import APIRouter
from api_fuctions.user_funcs import *

router = APIRouter(prefix="/user")


@router.post("/users/reg", response_model=None)
def register_user(data: Reg):
    return register(data)


@router.post("/users/auth", response_model=None)
def auth_user(data: Creds):
    return authorization(data)


@router.put("/change_username")
def change_username(new_username: str, data: Token):
    return username_change(new_username, data)
