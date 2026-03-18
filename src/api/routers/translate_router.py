from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException, Path
from src.tasks.tasks import translate_file_task

router = APIRouter(prefix="/translate", tags=["Перевод"])


@router.get(
    "/", summary="Перевести файл"
)
async def translate_file(
    input_path: str,
    output_path: str
):
    if not Path(input_path).is_file():
        raise HTTPException(404, detail="Исходный файл не найден")

    task = translate_file_task.delay(input_path, output_path)

    return {"status": "success", "details": 'Start file translate', "task_id": task.id}


@router.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task = translate_file_task.AsyncResult(task_id)
    if task.ready():
        return {"status": task.state, "result": task.result}
    return {"status": task.state}