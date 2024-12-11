from fastapi import FastAPI, status, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import Annotated
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/", response_class=HTMLResponse)
def get_main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/user/{user_id}", response_class=HTMLResponse)
def get_users(request: Request, user_id) -> HTMLResponse:
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})


@app.post("/user/{username}/{age}")
def create_user(user: User):
    if len(users) == 0:
        user.id = 1
    else:
        user.id = users[-1].id + 1
    users.append(user)
    return user


@app.put("/user/{user_id}/{username}/{age}")
def update_user(user_id: int, user: User):
    try:
        user.id = user_id
        user_upd = users[user.id - 1]
        user_upd.username = user.username
        user_upd.age = user.age
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")
    return user


@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    for i, u in enumerate(users):
        if u.id == user_id:
            user = users[i]
            del users[i]
            return user
    raise HTTPException(status_code=404, detail="User was not found")

# uvicorn module_16_5:app
