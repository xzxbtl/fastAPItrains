from typing import Optional

from fastapi import FastAPI, HTTPException
import json

app = FastAPI()
FILE_PATH = r'C:\Users\xzxbt\PycharmProjects\FastAPITraining\pythonProject1\firstlesson\donations.json'


@app.get("/")
async def home() -> dict[str, str | int]:
    return {"user": "xzxbtl", "ID": 2631}


@app.get("/contacts")
async def contacts() -> dict[str, int | list[str]]:
    with open(FILE_PATH, 'r') as f:
        all_contacts = json.load(f)
        count_contacts = len(list(all_contacts.keys()))

    return {"Count": count_contacts, "Users": list(all_contacts.keys())}


@app.get("/contacts/{user_name}")
async def user(user_name: str) -> dict:
    with open(FILE_PATH, 'r') as f:
        all_contacts = json.load(f)
        if user_name in all_contacts:
            return all_contacts[user_name]
        raise HTTPException(status_code=404, detail="User not found")


@app.get("/search")
async def search(order_id: Optional[int] = None) -> dict:
    if order_id is None:
        raise HTTPException(status_code=400, detail="order_id must be provided")

    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        all_contacts = json.load(f)
        for user_name, dates in all_contacts.items():
            for date, messages in dates.items():
                for message in messages:
                    payment_id = message.get("id")
                    if payment_id == order_id:
                        return {user_name: {"date": date, "payment_ID": payment_id}}

    raise HTTPException(status_code=404, detail="order_id not found")
