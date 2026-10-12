import os
from supabase import create_client, Client
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, Field
import bcrypt
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)

@app.post("/register")
def register_user(user: User):
    response = client.table("users").insert({"username": user.username, "password": user.password}).execute()
    return response


@app.post("/login")
def login_user(user: User):
    response = client.table("users").select("*").eq("username", user.username).eq("password", user.password).execute()
    return response


@app.post("/register_hashed")
def register_user_hashed(user: User):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    response = client.table("users").insert({"username": user.username, "password": hashed_password.decode('utf-8')}).execute()
    return response


@app.post("/login_hashed")
def login_user_hashed(user: User):
    response = client.table("users").select("*").eq("username", user.username).execute()
    if response.data and bcrypt.checkpw(user.password.encode('utf-8'), response.data[0]['password'].encode('utf-8')):
        return {"status": "success"}
    return {"status": "failure"}


SECRET_KEY = os.getenv("SECRET_KEY")
security = HTTPBearer()

@app.post("/login_for_access_token")
def login_for_access_token(user: User):
    if user.username == "admin" and user.password == "admin":
        access_token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm="HS256")
        return {"access_token": access_token}
    return {"error": "Invalid credentials"}


SECRET_KEY = os.getenv("SECRET_KEY")
security = HTTPBearer()
password_hash = PasswordHash.recommended()


@app.post("/register_hashed_pwdlib")
def register_user_hashed_pwdlib(user: User):
    hashed_password = password_hash.hash(user.password)
    response = client.table("users").insert({"username": user.username, "password": hashed_password}).execute()
    return response

@app.post("/login_hashed_pwdlib")
def login_user_hashed_pwdlib(user: User):
    response = client.table("users").select("*").eq("username", user.username).execute()
    if response.data and password_hash.verify(user.password, response.data[0]['password']):
        access_token = jwt.encode({"sub": user.username,
                                   "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=30)
                                   }, SECRET_KEY, algorithm="HS256")
        return {"status": "success", "access_token": access_token}
    return {"status": "failure"}


@app.get("/access_profile")
def access_profile(token = Depends(security)):
    decoded = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
    return {"status": "success", "username": decoded['sub']}

