#audit initiation and results

from fastapi import APIRouter

router = APIRouter(
    prefix="/audits",
    tags=["audits"],
)
