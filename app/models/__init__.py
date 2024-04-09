from typing import Union, Optional, List, Set, Dict

from pydantic import BaseModel, validator, Field
from pydantic_core.core_schema import FieldValidationInfo

import datetime


class ConverterRequest(BaseModel):
    number: Union[int, str]


class ConverterResponse(BaseModel):
    arabic: int
    roman: str


class User(BaseModel):
    name: str
    age: int
    adult: bool
    message: str = None

    @validator("age")
    @classmethod
    def validate_password(cls, value):
        if 0 <= value <= 100:
            return value
        raise ValueError('Возраст не может быть меньше 0 и больше 100.')

    @validator("adult")
    @classmethod
    def validate_adult(cls, v, values):
        if v and values['age'] >= 18 or not v and values['age'] < 18:
            return v
        raise ValueError('Несоответствие в возрасте.')


class Mapping(BaseModel):
    list_of_ids: List[Union[str, int]]
    tags: Set[str]
    

class Meta(BaseModel):
    last_modification: str
    list_of_skills: List[str] = None
    mapping: Mapping

    @validator("last_modification")
    @classmethod
    def validate_last_modification(cls, value):
        if bool(datetime.datetime.strptime(value, '%d/%m/%Y')):
            return value
        raise ValueError('Неверный формат даты.')


class BigJson(BaseModel):
    """Использует модель User."""
    user: User
    meta: Meta

class Task6Json(BaseModel):
    """Описание JSON"""
    file_type: str = Field(pattern='^(json|csv|yaml)$')
    matrix_size: int = Field(ge=4, le=15)

# class UserRequest(BaseModel):
#     name: str
#     message: str
#
#
# class User(BaseModel):
#     name: str
#     age: str
#     is_adult: bool
#     message: str = None
#
#
# class UserResponse(BaseModel):
#     pass
