from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Создаем модель пользователя
class User(BaseModel):
    username: str
    email: str


@app.post("/")
def create_user():
    # Получение данных из формы
    form_data = {
        "username": request.form["username"],
        "email": request.form["email"]
    }

    # Создание нового объекта User и отправка его на сервер
    new_user = User(**form_data)
    response.status_code = 201

    return new_user


@app.get("/users", response_model=List[User])
def read_users():
    # Возвращает пользователей из базы данных
    users = session.query(User).all()
    return users
