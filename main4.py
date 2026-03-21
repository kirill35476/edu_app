from fastapi import FastAPI
from models.models import Student

app = FastAPI()
students_db = []
book_db = []

@app.post("/student")
async  def create_student(student: Student):
    students_db.append(student)
    return {"message": f"Ученик {student.name} успешно создан!"}

@app.post("/book")
async def book(pages: str, author: str,data:int ,name_book:str):
    book_db.append(pages,author,data,name_book)
    return {"message": f"Книга {name_book}.Автор {author}.Дата выхода{data}.Кол-во страниц{pages}"}


