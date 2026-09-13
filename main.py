from fastapi import FastAPI
from database import engine, Base
from users import models
from users.router import router as users_router
from login import router as login_router

Base.metadata.create_all(bind = engine)

app = FastAPI( title ="FastAPI School App")

app.include_router(users_router)
app.include_router(login_router.router)

@app.get("/")
def read_root():
    return{"message" : "Welcome to the School API! The datebase is connected."}

