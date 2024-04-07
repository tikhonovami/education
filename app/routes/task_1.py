from fastapi import APIRouter


router = APIRouter(tags=["Стажировка"])


"""
Задание_1. Удаление дублей
    Реализуйте функцию соответствующую следующему описанию:
    На вход подаётся массив слов зависимых от регистра, для которых необходимо произвести
    фильтрацию на основании дублей слов, если в списке найден дубль по регистру, то все
    подобные слова вне зависимости от регистра исключаются.
    На выходе должны получить уникальный список слов в нижнем регистре.

    Список слов для примера: ['Мама', 'МАМА', 'Мама', 'папа', 'ПАПА', 'Мама', 'ДЯдя', 'брАт', 'Дядя', 'Дядя', 'Дядя']
    Ожидаемый результат: ['папа','брат']
"""
@router.post("/find_in_different_registers", description="Задание_1. Удаление дублей")
async def find_in_different_registers(words: list[str]) -> list[str]:
    """
    Input:
    words: list[str] - список слов, в котором необходимо произвести
    фильтрацию.
    Output:
    result: list[str] - уникальный список слов в нижнем регистре.
    """
    lower_words = dict()
    result = []

    for word in words:
        lower_word = word.lower()

        if lower_word not in lower_words:
            lower_words[lower_word] = [word]
            continue

        if word in lower_words[lower_word]:
            lower_words[lower_word] = []
            continue

        if lower_words[lower_word]:
            lower_words[lower_word].append(word)

    result = [key for key, value in lower_words.items() if value]
    return result
