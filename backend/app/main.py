from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine
from db import models

app = FastAPI()
origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return {
        "message": "Hello World"
    }

models.Base.metadata.create_all(engine)