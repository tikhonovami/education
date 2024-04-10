from fastapi import APIRouter, Response, Request
from functools import wraps

router = APIRouter(tags=["Стажировка"])

"""
Задание_8. Декоратор - счётчик запросов.

Напишите декоратор который будет считать кол-во запросов сделанных к приложению.
Оберните роут new_request() этим декоратором.
Подумать, как хранить переменную с кол-вом сделаных запросов.
"""
count_of_requests = 0


def count_requests(func):
    @wraps(func)
    async def wrapper():
        global count_of_requests
        count_of_requests += 1
        res = func()
        return await res
    return wrapper


@router.get("/new_request", description="Задание_8. Декоратор - счётчик запросов.")
@count_requests
async def new_request():
    """Возвращает кол-во сделанных запросов."""
    return count_of_requests
