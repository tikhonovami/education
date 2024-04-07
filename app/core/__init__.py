from abc import ABC, abstractmethod
from io import StringIO


def convert_arabic_to_roman(number: int, i: int = -1, res: str = '') -> str:
    '''
    Функция переводит арабское число в римское.

    Input:
    number: int - арабское число,
    i: int = -1 - указатель на базовое значение,
    res: str = '' - результат (римское число),

    Output:
    res: str = '' - результат (римское число).
    '''
    nums = [1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000]
    values = ['I', 'IV', 'V', 'IX', 'X', 'XL', 'L', 'XC', 'C', 'CD', 'D', 'CM', 'M']

    if not number:
        return res

    div = number // nums[i]
    number %= nums[i]

    res += div * values[i]

    return convert_arabic_to_roman(number, i - 1, res)


def convert_roman_to_arabic(number: str) -> int:
    '''
    Функция переводит римское число в арабское.
    
    Input:
    number: str - римское число,

    Output:
    res: int - арабское число.
    '''
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    subtracted_values = {'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90, 'CD': 400, 'CM': 900}
    res = 0

    for key, value in subtracted_values.items():
        if number.find(key) > -1:
            number = number.replace(key, '')
            res += value
            
    for symbol in number:
        res += values[symbol]
    return res


def average_age_by_position(file):
    pass


"""
Задание_6.
Дан класс DataGenerator, который имеет два метода: generate(), to_file()
Метод generate генерирует данные формата list[list[int, str, float]] и записывает результат в
переменную класса data
Метод to_file сохраняет значение переменной generated_data по пути path c помощью метода
write, классов JSONWritter, CSVWritter, YAMLWritter.

Допишите реализацию методов и классов.
"""
class BaseWriter(ABC):
    """Абстрактный класс с методом write для генерации файла"""

    @abstractmethod
    def write(self, data: list[list[int, str, float]]) -> StringIO:
        """
        Записывает данные в строковый объект файла StringIO
        :param data: полученные данные
        :return: Объект StringIO с данными из data
        """
        pass


class JSONWriter(BaseWriter):
    """Потомок BaseWriter с переопределением метода write для генерации файла в json формате"""

    """Ваша реализация"""

    pass


class CSVWriter:
    """Потомок BaseWriter с переопределением метода write для генерации файла в csv формате"""

    """Ваша реализация"""

    pass


class YAMLWriter:
    """Потомок BaseWriter с переопределением метода write для генерации файла в yaml формате"""

    """Ваша реализация"""

    pass


class DataGenerator:
    def __init__(self, data: list[list[int, str, float]] = None):
        self.data: list[list[int, str, float]] = data
        self.file_id = None

    def generate(self, matrix_size) -> None:
        """Генерирует матрицу данных заданного размера."""

        data: list[list[int, str, float]] = []
        """Ваша реализация"""

        self.data = data

    def to_file(self, path: str, writer) -> None:
        """
        Метод для записи в файл данных полученных после генерации.
        Если данных нет, то вызывается кастомный Exception.
        :param path: Путь куда требуется сохранить файл
        :param writer: Одна из реализаций классов потомков от BaseWriter
        """

        """Ваша реализация"""

        pass
