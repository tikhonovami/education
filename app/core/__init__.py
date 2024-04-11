from abc import ABC, abstractmethod
from io import StringIO
from fastapi import HTTPException

from pandas import read_csv
from string import ascii_lowercase

import csv
import json
import yaml

from typing import Dict
from os import path, popen
from random import choice, uniform


def convert_arabic_to_roman(number: int, i: int = -1, res: str = "") -> str:
    """
    Переводит арабское число в римское.
    :param number: арабское число,
    :param i: указатель на базовое значение,
    :param res: результат (римское число).
    
    :return res: результат (римское число).
    """
    nums = [1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000]
    values = ["I", "IV", "V", "IX", "X", "XL", "L", "XC", "C", "CD", "D", "CM", "M"]

    if not number:
        return res

    div = number // nums[i]
    number %= nums[i]
    res += div * values[i]

    return convert_arabic_to_roman(number, i - 1, res)


def convert_roman_to_arabic(number: str) -> int:
    """
    Переводит римское число в арабское.
    :param number: римское число,
    :return res:арабское число.
    """
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    sub_values = {"IV": 4, "IX": 9, "XL": 40, "XC": 90, "CD": 400, "CM": 900}
    res = 0

    for key, value in sub_values.items():
        if number.find(key) > -1:
            number = number.replace(key, "")
            res += value

    for symbol in number:
        res += values[symbol]

    return res


def average_age_by_position(file: str) -> Dict[str, float]:
    """
    Возвращает средний возраст сотрудников на каждой должности.
    :param file: название файла в формате <название>.csv (файл
    должен быть в папке files).
    :return: данные о среднем возрасте сотрудников на каждой
    должности.
    """
    file = r"app/files/" + file

    if path.splitext(file)[1] != ".csv":
        raise HTTPException(
            status_code=400,
            detail="Неверный формат файла.")

    with open(file, "r", encoding="utf-8") as f:
        data = read_csv(f, delimiter=",")
        
        rows = data.columns.values.tolist()
        correct_rows = ["Имя", "Возраст", "Должность"]

        if (len(rows) != len(correct_rows) or
            not all([bool(correct_rows[i] == rows[i]) 
                     for i in range(len(correct_rows))])):
            raise HTTPException(
                status_code=400,
                detail="Неверное содержимое файла.")
                
        data = data.groupby("Должность")["Возраст"].mean().fillna("null")

        return data.to_dict()


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
    def __init__(self):
        pass
        
    @abstractmethod
    def write(self, data: list[list[int, str, float]]) -> StringIO:
        """
        Записывает данные в строковый объект файла StringIO
        :param data: полученные данные
        :return: Объект StringIO с данными из data
        """
        output = StringIO()
        output.write(str(data))
        return output


class JSONWriter(BaseWriter):
    """Потомок BaseWriter с переопределением метода write для генерации файла
    в json формате
    """

    def write(self, data: list[list[int, str, float]]) -> StringIO:
        """
        Записывает данные в строковый объект файла StringIO
        :param data: полученные данные
        :return: Объект StringIO с данными из data
        """
        json_str = json.dumps([{"int": d[0], "str": d[1], "float": d[2]} 
                              for d in data])
        return StringIO(json_str)


class CSVWriter(BaseWriter):
    """Потомок BaseWriter с переопределением метода write для генерации файла
    в csv формате
    """

    def write(self, data: list[list[int, str, float]]) -> StringIO:
        """
        Записывает данные в строковый объект файла StringIO
        :param data: полученные данные
        :return: Объект StringIO с данными из data
        """
        io_obj = StringIO()
        data.insert(0, ["int", "str", "float"])
        csv_str = csv.writer(io_obj, delimiter=",", lineterminator="\n")
        csv_str.writerows(data)
        return io_obj


class YAMLWriter(BaseWriter):
    """Потомок BaseWriter с переопределением метода write для генерации файла
    в yaml формате
    """

    def write(self, data: list[list[int, str, float]]) -> StringIO:
        """
        Записывает данные в строковый объект файла StringIO
        :param data: полученные данные
        :return: Объект StringIO с данными из data
        """
        yaml_str = yaml.dump([{"int": d[0], "str": d[1], "float": d[2]} 
                             for d in data])
        return StringIO(yaml_str)


class NoDataException(HTTPException):
    def __init__(self, detail: str = "Нет данных.", status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class DataGenerator:
    def __init__(self, data: list[list[int, str, float]] = None):
        self.data: list[list[int, str, float]] = data
        self.file_id: int | None = None

    def generate(self, matrix_size) -> None:
        """Генерирует матрицу данных заданного размера."""

        data: list[list[int, str, float]] = []

        for i in range(matrix_size):
            random_word = "".join([choice(ascii_lowercase) for _ in range(5)])
            random_float = uniform(0.0, 100.0)
            data.append([i, random_word, random_float])
            
        self.data = data

    def to_file(self, path: str, writer: str) -> None:
        """
        Метод для записи в файл данных полученных после генерации.
        Если данных нет, то вызывается кастомный Exception.
        :param path: Путь куда требуется сохранить файл
        :param writer: Одна из реализаций классов потомков от BaseWriter
        """

        if not self.data:
            raise NoDataException
        
        if writer == "json":
            item = JSONWriter()
        elif writer == "yaml":
            item = YAMLWriter()
        else:
            item = CSVWriter()

        io_item = item.write(self.data)
        full_path = path + "/data." + writer
        
        with open(full_path, "w") as f:
            f.write(io_item.getvalue())
        
        self.file_id = int(popen(fr'fsutil file queryfileid "{full_path}"').read().split(":")[-1].strip(), 16)
        return
