from fastapi import APIRouter
from api_fuctions.game import *

router = APIRouter()


@router.post('/game')
def create_game(user_id: int):
    # Сюда функция для создания игры + вернуть её идентификатор
    return create_game_func()


@router.get('/game/{game_id}')
def get_game(game_id: int):
    # Получить игру по идентификатору
    return get_game_func()


@router.post('/game/{game_id}/move')
def make_move(game_id: int, move: str):
    # Сделайте ход в игре
    return make_move_func()
