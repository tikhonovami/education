from typing import Annotated

from fastapi import APIRouter, Body, HTTPException

from app.core import convert_arabic_to_roman, convert_roman_to_arabic
from app.models import ConverterResponse

import re


router = APIRouter(tags=["Стажировка"])

"""
Задание_2. Конвертер
    1. Реализовать функции convert_arabic_to_roman() и convert_roman_to_arabic() из пакета app.core
    2. Написать логику и проверки для вводимых данных. Учитывать, что если арабское число выходит за пределы 
    от 1 до 3999, то возвращать "не поддерживается"
    3. Запустить приложение и проверить результат через swagger
"""
@router.post("/converter", description="Задание_2. Конвертер")
async def convert_number(number: Annotated[int | str, Body()]) -> ConverterResponse:
    """
    Принимает арабское или римское число.
    Конвертирует его в римское или арабское соответственно.
    Возвращает первоначальное и полученное числа в виде json:
    {
        "arabic": 10,
        "roman": "X"
    }
    """

    if isinstance(number, int):
        if 1 <= number <= 3999:
            converter_response = ConverterResponse(
                arabic=number,
                roman=convert_arabic_to_roman(number))
        else:
            raise HTTPException(
                status_code=400,
                detail="не поддерживается.")
    else:
        template = r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
        if not (bool(re.search(template, number))):
            raise HTTPException(
                status_code=400,
                detail="римское число введено неверно.")
        converter_response = ConverterResponse(
            arabic=convert_roman_to_arabic(number),
            roman=number)

    return converter_response
