from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory='app/templates')

# Подключение маршрутов
from app.routers import task

app.include_router(task.router)

@app.get("/", include_in_schema=False)
async def redirect_to_tasks():
    return RedirectResponse(url="/tasks/")