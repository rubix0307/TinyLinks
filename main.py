import hashlib
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

links = {
    'test': 'https://google.com',
}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
def create(request: Request, full_link: str = Form()):
    short_link = hashlib.sha256(full_link.encode()).hexdigest()[:10]
    links.update({short_link: full_link})
    return templates.TemplateResponse("index.html", {"request": request, "short_link": short_link})


@app.get("/{short_link}", name='redirect_short_link')
def redirect(short_link: str):
    redirect_url = links.get(short_link)
    if redirect_url:
        return RedirectResponse(url=redirect_url)
    return {'result': 'link not found'}
