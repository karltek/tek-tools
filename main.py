from time import sleep

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from fastapi_utils.tasks import repeat_every
import httpx

app = FastAPI(docs_url=None, redoc_url=None)

# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# @app.on_event("startup") is deprecated and needs to be fixed using Lifespan as per FastAPI docs
@app.on_event("startup")
@repeat_every(seconds=600)  # 10 minutes
async def render_inactivity_fix():
    url = "https://tek-tools.onrender.com/"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            print(f"Pinged at {response.status_code}")
    except httpx.RequestError as exc:
        print(f"An error occurred: {exc}")


# Add options for IPv6 , custom separator
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html",
    )