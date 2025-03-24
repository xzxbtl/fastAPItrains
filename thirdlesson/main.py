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


class PostCreate(BaseModel):
    title: str
    body: str
    author_id: int


@app.get("/items")
async def items() -> List[Post]:
    return [Post(**post) for post in posts]


@app.post("/items/add")
async def add_item(post: PostCreate) -> Post:
    author = next((user for user in users if user['user_id'] == post.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    new_post_id = len(posts) + 1
    new_post = {'id': new_post_id, 'title': post.title, 'body': post.body, 'author': author}
    posts.append(new_post)

    return Post(**new_post)


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
