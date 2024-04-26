from fastapi import APIRouter
from api.users import router as user_router
from api.game import router as game_router

router = APIRouter()
router.include_router(user_router)
router.include_router(game_router)

