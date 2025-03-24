from fastapi import FastAPI, HTTPException
from typing import Optional, List, Dict
from pydantic import BaseModel

app = FastAPI()

users = [
    {'user_id': 0, 'username': '@santy', 'age': 21},
    {'user_id': 1, 'username': '@q1s00', 'age': 15},
    {'user_id': 2, 'username': '@xzxbtl', 'age': 44},
]

posts = [
    {'id': 0, 'title': 'New1', 'body': 'HTML1', 'author': users[0]},
    {'id': 1, 'title': 'ALEXANDRA??', 'body': 'Привет, а ты ниче такая \n Шучу уже здоровались', "author": users[1]},
    {'id': 2, 'title': 'New3', 'body': 'HTML3', 'author': users[2]},
]


class User(BaseModel):
    user_id: int
    username: str
    age: int


class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User


@app.get("/items")
async def items() -> List[Post]:
    return [Post(**post) for post in posts]


@app.get("/items/{id}")
async def item_id(id: int) -> Post:
    for post in posts:
        if post['id'] == id:
            return Post(**post)
    raise HTTPException(status_code=404, detail="Item not found")


@app.get('/search')
async def search(post_id: Optional[int] = None) -> Dict[str, Optional[Post]]:
    if post_id:
        for post in posts:
            if post['id'] == post_id:
                return {"data": Post(**post)}
        raise HTTPException(status_code=404, detail="Item not found")
    return {"data": None}


"""
@app.get("/items")
async def items() -> List[Post]:
    post_objects = []
    for post in posts:
        post_objects.append(Post(id=post['id'], title=post['title'], body=post['body']))
    return post_objects
"""
