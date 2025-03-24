from fastapi import FastAPI, HTTPException, Body, Depends
from typing import List, Annotated, Type
from sqlalchemy.orm import Session
from models import Base, User, Post
from database import engine, session_local
from schemas import UserCreate, User as DbUser, PostCreate, PostResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=DbUser)
async def create_user(user: Annotated[
    UserCreate,
    Body(
        ..., example={
            "username": "UserName",
            "age": 21
        }
    )], db: Session = Depends(get_db)) -> DbUser:
    db_user = User(username=user.username, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/posts/", response_model=PostResponse)
async def create_post(post: Annotated[
    PostCreate,
    Body(
        ..., example={
            "title": "Title",
            "body": "Content",
            "author_id": 12
        }
    )
], db: Session = Depends(get_db)) -> PostResponse:
    db_user = db.query(User).filter(User.user_id == post.author_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_post = Post(title=post.title, body=post.body, author_id=post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@app.get("/posts/", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()


@app.get("/", response_model=List[DbUser])
async def main(db: Session = Depends(get_db)) -> list[Type[DbUser]]:
    users = db.query(User).all()
    return users


"""
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
async def items_id(id: Annotated[int, Path(..., title='Указывается ID поста', ge=0, lt=100)]) -> Post:
    for post in posts:
        if post['id'] == id:
            return Post(**post)
    raise HTTPException(status_code=404, detail="Item not found")


@app.get('/search')
async def search(post_id: Annotated[
    Optional[int],
    Query(title='ID of post to search for post', gt=0, le=100)
]) -> Dict[str, Optional[Post]]:
    if post_id:
        for post in posts:
            if post['id'] == post_id:
                return {"data": Post(**post)}
        raise HTTPException(status_code=404, detail="Item not found")
    return {"data": None}


@app.post("/user/add")
async def user_add(user: Annotated[
    UserCreate,
    Body(..., example={
        "username": "UserName",
        "age": 21
    })
]) -> User:
    new_user_id = len(users) + 1
    new_user = {'user_id': new_user_id, 'username': user.username, 'age': user.age}
    users.append(new_user)

    return User(**new_user)



@app.get("/items")
async def items() -> List[Post]:
    post_objects = []
    for post in posts:
        post_objects.append(Post(id=post['id'], title=post['title'], body=post['body']))
    return post_objects
"""
