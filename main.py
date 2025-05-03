from fastapi import FastAPI
from app.routes.api import router

app = FastAPI(title="APP de Fondos de Inversión")
app.include_router(router)