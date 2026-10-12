import os
from supabase import create_client, Client
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.get("/students")
def get_students():
    response = client.table("students").select("*").execute()
    return response.data

@app.get("/students/{student_id}")
def get_student_by_id(student_id: int):
    response = client.table("students").select("*").eq("id", student_id).execute()
    return response.data

@app.get("/students/age/{age}")
def filter_by_age(age: int):
    response = client.table("students").select("*").eq("age", age).execute()
    return response.data


class Student(BaseModel):
    name: str = Field(ge=1, le=100)
    email: EmailStr
    age: int = Field(ge=18, le=100)
    course: str

@app.post("/students/insert")
def insert_student(student: Student):
    response = client.table("students").insert(student.model_dump()).execute()
    return response.data

