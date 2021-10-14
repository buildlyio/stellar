from fastapi import Depends, FastAPI

from routers import login, accounts, payment

app = FastAPI()


app.include_router(login.router)
app.include_router(accounts.router)
app.include_router(payment.router)

@app.get("/")
async def root():
    return {"message": "Hello Meowcoin!"}
