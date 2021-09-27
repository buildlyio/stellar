from fastapi import APIRouter
from fastapi import FastAPI, Form

router = APIRouter()

@router.get("/login/", tags=["login"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
