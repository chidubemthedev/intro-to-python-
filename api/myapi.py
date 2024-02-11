from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name": "john",
        "age": 17,
        "year": "year 12"
    }
}

class Student(BaseModel):
    name: str
    age: int
    year: str
    
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

@app.get("/")
def read_root():
    return {"name": "Valentine from FastAPI"}

@app.get("/students/get-all")
def get_students():
    return students

@app.get("/students/{student_id}")
def read_student(student_id: int = Path(..., description="The ID of the student you want to view", gt=0, lt=5)):
    if student_id not in students:
        return {"Error": "Student not found."}
    return students[student_id]

@app.get("/student/get-by-name/{student_id}")
def get_student(*, student_id: int, name: Optional[str] = None, test: int = 10):
    if name is None:
        return {"Data": "No name provided"}
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not found"}

@app.post("/student/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student exists"}
    students[student_id] = student
    return students[student_id]

@app.put("/student/update/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student not found."}
    
    if student.name != None:
        students[student_id].name = student.name
        
    if student.age != None:
        students[student_id].age = student.age
        
    if student.year != None:
        students[student_id].year = student.year
        
    return students[student_id]

@app.delete("/student/delete/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student not found."}
    del students[student_id]
    return {"Message": "Student deleted successfully."}