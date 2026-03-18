from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="ChecAI API")
app.include_router(router)
