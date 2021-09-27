from fastapi import Depends, FastAPI

from routers import login, accounts

app = FastAPI()


app.include_router(login.router)
app.include_router(accounts.router)

@app.get("/")
async def root():
    return {"message": "Hello Meowcoin!"}
