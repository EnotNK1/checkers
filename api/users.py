from fastapi import APIRouter
from api_fuctions.user_funcs import *


router = APIRouter(prefix="/users")


@router.post("/reg", response_model=None)
def register_user(data: Reg):
    return register(data)


@router.post("/auth", response_model=None)
def auth_user(data: Creds):
    return authorization(data)


@router.put("/change_username")
def change_username(new_username: str, data: Token):
    return username_change(new_username, data)
