from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class User(BaseModel):
    username: str
    email: EmailStr


class UserSchema(User):
    password: str


class UserBD(UserSchema):
    id: int


class UserPublic(User):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]
