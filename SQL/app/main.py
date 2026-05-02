from fastapi import FastAPI
from app.routers import cars, services

app = FastAPI()

app.include_router(cars.router)
app.include_router(services.router)
