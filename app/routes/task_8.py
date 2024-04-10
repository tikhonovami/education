from fastapi import APIRouter, Response, Request
from functools import wraps
from os import path

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
        file_path = "app\\files\\count.txt"
        if not path.exists(file_path) or path.getsize(file_path) == 0:
            with open(file_path, 'w') as f:
                f.write('0')
        with open(file_path, 'r') as f: 
            count_of_requests = int(f.read()) + 1
        with open(file_path, 'w') as f: 
            f.write(str(count_of_requests))
        res = func()
        return await res
    return wrapper


@router.get("/new_request", description="Задание_8. Декоратор - счётчик запросов.")
@count_requests
async def new_request():
    """Возвращает кол-во сделанных запросов."""
    return count_of_requests
