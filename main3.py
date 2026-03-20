from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/user/{username}")
async def greet_user(username: str):
    return {"message": f"Hello, {username}!"}

@app.get("/age/{years}")
async def age_converter(years: int):
    return {"years": years, "months": years * 12, "days": years * 365}

@app.get("/grade/{score}")
async def grade_converter(score: int):
    if score >= 90: grade = 5
    elif score >= 75: grade = 4
    elif score >= 60: grade = 3
    elif score >= 40: grade = 2
    else: grade = 1
    return {"score": score, "grade": grade}

@app.get("/cm-to-inches")
async def cm_to_inches(cm: float):
    return {"centimeters": cm, "inches": round(cm / 2.54, 2)}

@app.get("/kg-to-lbs")
async def kg_to_lbs(kg: float):
    return {"kilograms": kg, "pounds": round(kg * 2.20462, 2)}

@app.get("/c-to-f")
async def c_to_f(c: float):
    return {"celsius": c, "fahrenheit": round(c * 9/5 + 32, 2)}


grades_db = []

# grades_db = [
#     {"subject": "Math", "score": 5, "student": "Alice"},
#     {"subject": "Russian", "score": 4, "student": "Alice"},
#     {"subject": "Physics", "score": 5, "student": "Alice"},
#     {"subject": "Math", "score": 3, "student": "Bob"}
# ]

class Grade(BaseModel):
    subject: str
    score: int
    student: str

@app.get("/average-grade/{student}")
async def average_grade(student: str):
    student_grades = [g["score"] for g in grades_db if g["student"] == student]
    if not student_grades:
        return {"student": student, "average": None, "message": "No grades found"}
    return {"student": student, "average": round(sum(student_grades) / len(student_grades), 2)}

@app.get("/subjects/{student}")
async def student_subjects(student: str):
    subjects = {g["subject"]: g["score"] for g in grades_db if g["student"] == student}
    if not subjects:
        return {"student": student, "message": "No subjects found"}
    return {"student": student, "subjects": subjects}

@app.post("/add-grade")
async def add_grade(grade: Grade):
    if grade.score < 1 or grade.score > 5:
        return {"error": "Score must be between 1 and 5"}
    grades_db.append(grade.model_dump())
    return {"message": "Grade added", "grade": grade}
