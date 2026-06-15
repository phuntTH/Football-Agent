from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, "ui"))

from fastapi import Request

from api.chat import router

app = FastAPI()

app.include_router(router)

app.mount(
    "/static",
    StaticFiles(directory="ui/static"),
    name="static"
)

templates = Jinja2Templates(
    directory="ui/templates"
)


@app.get("/")
async def home(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )