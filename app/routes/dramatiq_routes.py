from fastapi import APIRouter
from fastapi import status

from app.background_tasks.example_task import example_task
router = APIRouter(tags=["background-process"])

@router.post(
    "/example",
    response_model=str,
    status_code=status.HTTP_200_OK,
)
async def login(
) -> str:
    example_task.send()
    return "background task scheduled for execution."