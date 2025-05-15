from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine
from app.routers import reports, audits, contracts
from app import models

app = FastAPI()
app.include_router(reports.router)
app.include_router(contracts.router)
app.include_router(audits.router)

origins = [
    "http://localhost:3000",
    #frontend url
]

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