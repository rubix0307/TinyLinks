from hashlib import md5
from typing import Annotated
import bson
from fastapi import Depends, HTTPException, status, FastAPI, Request, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from common import create_short_url, get_long_url, update_short_url
from mongo_db import db

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def simple_hash_password(password: str):
    return md5(password.encode('utf-8')).hexdigest()

async def get_user_by_token(token: str):
    user_dict = await db.user.find_one({'_id': bson.ObjectId(token)})
    if user_dict:
        return UserInDB(**user_dict)


async def fake_decode_token(token):
    user = await get_user_by_token(token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = await fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = await db.user.find_one({'username': form_data.username})
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = simple_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = str(user_dict['_id'])
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

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


