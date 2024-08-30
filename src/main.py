from fastapi import FastAPI

from src.router import phone_router

app = FastAPI()
app.include_router(phone_router)






