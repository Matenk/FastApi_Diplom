from fastapi import APIRouter, Depends, status, HTTPException, Request, Form
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse

from app.backend.db_depends import get_db
from typing import Annotated

from app.main import templates
from app.models.tasks import Tasks
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/tasks', tags=['tasks'])

@router.get("/", response_class=HTMLResponse)
async def read_tasks(request: Request, db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Tasks)).all()  # Получаем все задачи из базы данных
    return templates.TemplateResponse("create_task.html", {"request": request, "tasks": tasks})



@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)],
                      title: str = Form(),
                      content: str = Form(),
                        priority: int = Form()
                      ):
    try:
        db.execute(insert(Tasks).values(title=title,
                                       content=content,
                                       priority=priority,
                                       slug=slugify(title)))
        db.commit()
        return RedirectResponse(url="/tasks/", status_code=status.HTTP_303_SEE_OTHER)

    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Task already exists!'
        )


@router.post('/update_task')
async def update_task(db: Annotated[Session, Depends(get_db)],
                      task_id: int,
                      title: str = Form(),
                      content: str = Form(),
                      priority: int = Form()
                      ):
    task = db.scalar(select(Tasks).where(Tasks.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )

    db.execute(update(Tasks).where(Tasks.id == task_id).values(
        title=title,
        content=content,
        priority=priority
    ))
    db.commit()
    return RedirectResponse(url="/tasks/", status_code=status.HTTP_303_SEE_OTHER)


@router.post('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Tasks).where(Tasks.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )

    db.execute(delete(Tasks).where(Tasks.id == task_id))
    db.commit()
    return RedirectResponse(url="/tasks/", status_code=status.HTTP_303_SEE_OTHER)




