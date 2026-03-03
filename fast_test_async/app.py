from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fast_test_async.schemas import (
    Message,
    UserBD,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI(title="Estudando API!")

database: list[UserBD] = []


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root() -> dict[str, str]:
    return {"message": "Ola Mundo!"}


@app.get(
    "/health_check", status_code=HTTPStatus.OK, response_class=HTMLResponse
)
def health_check() -> str:
    return """
            <html>
                <body>
                    <h1> Olá </h1>
                </body>
            </html>
        """


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema) -> UserBD:
    user_with_id = UserBD(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id


@app.get("/users/", status_code=HTTPStatus.OK, response_model=UserList)
def read_users() -> dict[str, list[UserBD]]:
    return {"users": database}


@app.get(
    "/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user(user_id: int) -> UserBD:
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User Not Found",
        )

    return database[user_id - 1]


@app.put(
    "/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema) -> UserBD:
    user_with_id = UserBD(**user.model_dump(), id=user_id)
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User Not Found",
        )

    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete("/users/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int) -> dict[str, str]:
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User Not Found",
        )

    database.pop(user_id - 1)

    return {"operation": "Successfully"}
