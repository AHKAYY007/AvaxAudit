#report generation and export 

from fastapi import APIRouter

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)