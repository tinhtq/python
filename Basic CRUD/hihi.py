from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
data = [1, 2, 3, 4, 5, 6, 7, 8]


class User(BaseModel):
    username: str
    password: str
    name: str


@app.post("/get_item/")
def get_data(user: User):
    return user
