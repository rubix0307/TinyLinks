from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from common import create_short_url, get_long_url, update_short_url

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def create(long_link: str = Form(),  custom_short_url: str = Form(None)):
    answer = await create_short_url(long_link, custom_short_url=custom_short_url)
    return answer

@app.get("/{short_link}", name='redirect_short_link')
async def redirect(short_link: str):

    redirect_url = await get_long_url(short_link)
    if 'long_url' in redirect_url:
        return RedirectResponse(url=redirect_url['long_url'])
    return {'result': 'link not found'}

@app.post("/{short_link}", name='update_short_link')
async def update(short_url: str, new_long_url: str = Form()):
    answer = await update_short_url(short_url, new_long_url)
    return answer


