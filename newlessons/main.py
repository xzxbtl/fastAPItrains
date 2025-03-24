from typing import Any, Dict

import uvicorn
from pydantic.types import Annotated
from fastapi import FastAPI, Path

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "The Hobbit",
        "author": "Mathe",
    },
    {
        "id": 2,
        "title": "The Elden SkyRim",
        "author": "Washington",
    }
]


@app.get("/", summary="Главный Root", tags=["Основные Root"])
async def home():
    return 'Hello!'


@app.get("/books")
async def read_books():
    return books


@app.get("/books/{id}")
async def get_book(id: Annotated[int, Path(
    ..., title="ID книги", ge=1, lt=100
)]) -> Dict[str, Any]:

    for book in books:
        if book["id"] == id:
            return book


# uvicorn main:app --host 0.0.0.0 --port 8000

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=9021)
