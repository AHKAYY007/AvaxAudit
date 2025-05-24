from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine
from app.routers import reports, audits, contracts, vulnerabilities
from app import models

app = FastAPI()
app.include_router(reports.router)
app.include_router(contracts.router)
app.include_router(audits.router)
app.include_router(vulnerabilities.router)

origins = [
    "http://localhost|:3000",
    "http://localhost:8080",
    "https://avaxaudit.vercel.app/"
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

# models.Base.metadata.create_all(engine)