from fastapi import APIRouter
from api.users import router as user_router

router = APIRouter()
router.include_router(user_router)

