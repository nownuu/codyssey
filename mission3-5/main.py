from fastapi import FastAPI
from database import engine
from models import Base

app = FastAPI()

@app.on_event('startup')
def on_startup():
    Base.metadata.create_all(bind=engine)
