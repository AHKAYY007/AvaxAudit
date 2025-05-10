#contract upload/fetch

from fastapi import APIRouter

router = APIRouter(
    prefix="/contracts",
    tags=["contracts"],
)