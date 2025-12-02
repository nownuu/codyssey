from fastapi import FastAPI
from domain.question.question_router import router as question_router

app = FastAPI()

app.include_router(question_router)
