from pydantic import BaseModel,EmailStr,Field
from typing import Optional

class Student(BaseModel):
    name: str = Field(description = "Имя ученика",
                      min_lenght = 2,
                      max_lenght = 20,
                      example = "Иван Петров")
    age: str= Field(description = "Возраст в годах",
                    ge = 17,
                    le = 25,
                    example = 18)
    email: str
    grade: int
    hobby: str = Field(None,description = "Любимое занятие")
    phone: int = Field(None,description = "Телефон для связи",example = "+7-999-123-45-67")

class Book(BaseModel):
    name_dook: str
    author: str
    data: int
    pages: int
    library: bool= True


class Monster(BaseModel):
    name: str = Field(...,min_lenght = 2,max_lenght= 50)
    type: str
    power: int = Field(...,ge = 1,le= 100)
    hp: int = Field(...,ge =- 1,le =1000)
    is_rare: bool = False

class MonsterUpdate(BaseModel):
    """Модель для обновления (все поля необязательные)"""
    name: Optional[str] = None
    type: Optional[str] = None
    power: Optional[int] = None
    hp: Optional[int] = None
    is_rare: Optional[bool] = None