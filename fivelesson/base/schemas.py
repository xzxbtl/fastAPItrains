from typing import Annotated

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: Annotated[
        str, Field(..., title='Имя пользователя', min_length=2, max_length=30)
    ]
    age: Annotated[
        int, Field(..., title='Возраст пользователя', ge=1, le=120)
    ]


class UserCreate(UserBase):
    ...


class User(UserBase):
    user_id: Annotated[
        int, Field(..., title='ID Пользователя', ge=1)
    ]

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: Annotated[
        str, Field(..., title='Название Поста', min_length=2, max_length=100)
    ]
    body: Annotated[
        str, Field(..., title='Описание Поста')
    ]
    author_id: Annotated[
        int, Field(..., title='ID Пользователя', ge=1)
    ]


class PostCreate(PostBase):
    ...


class PostResponse(PostBase):
    id: Annotated[
        int, Field(..., title='ID поста', ge=1)
    ]
    author: User

    class Config:
        from_attributes = True
