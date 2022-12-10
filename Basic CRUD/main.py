from fastapi import FastAPI, Response, status
from pydantic import BaseModel, EmailStr
from datetime import datetime
import motor.motor_asyncio
from pprint import pprint
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

app = FastAPI()
mongoURI = "mongodb://192.168.239.131:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(mongoURI)
db = client.learnapi
collection_users = db.get_collection("users")


class User(BaseModel):
    fullname: str
    password: str
    email: EmailStr
    created_at: datetime = datetime.now().strftime("%a, %d %b %Y  %H:%M:%S %z")
    updated_at: datetime = datetime.now().strftime("%a, %d %b %Y  %H:%M:%S %z")

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Michael Tayson",
                "password": "***",
                "email": "Michael@gmail.com",
                "create_at": "2008-09-15 15:53:00+05:00",
                "update_at": "2008-09-15 15:53:00+05:00",
            }
        }


class Update_user(BaseModel):
    fullname: str
    updated_at: datetime = datetime.now().strftime("%a, %d %b %Y  %H:%M:%S %z")


def ResponeModel(data, message, respone, code):
    respone.status_code = code
    return {"data": [data], "message": message}


def ErrResponeModel(error, message, respone, code):
    respone.status_code = code
    return {"error": error, "message": message}


def ConvertData(user) -> dict:
    return {
        "id": str(user["_id"]),
        "fullname": user["fullname"],
        "email": user["email"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"],
    }


# Register
@app.post("/users/register")
async def create_user(user: User, response: Response):
    data = jsonable_encoder(user)
    add_user = await collection_users.insert_one(data)
    new_user = await collection_users.find_one({"_id": add_user.inserted_id})
    pprint(type(new_user))
    return ResponeModel(ConvertData(new_user), "Successfully added", response, 201)


# List all users
@app.get("/users")
async def list_user(response: Response):
    users = []
    async for user in collection_users.find():
        users.append(ConvertData(user))
    if users:
        return ResponeModel(users, "Data Retrived", response, 202)


# Get info user
@app.get("/users/{id}")
async def get_users(id: str, response: Response):
    try:
        user = await collection_users.find_one({"_id": ObjectId(id)})
    except:
        return ErrResponeModel("An error", "Invalid Request", response, 404)
    if user:
        return ResponeModel(ConvertData(user), "Data", response, 200)
    else:
        return ErrResponeModel("An error", "User not found", response, 404)


# Update user
@app.put("/users/{id}")
async def update_user(info_update: Update_user, id: str, response: Response):
    try:
        data = jsonable_encoder(info_update)
        pprint(data)
        check_update = await collection_users.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if check_update.modified_count == 1:
            user = await collection_users.find_one({"_id": ObjectId(id)})
            return ResponeModel(ConvertData(user), "Data", response, 200)
        else:
            return ErrResponeModel("An error", "Wrong information", response, 404)
    except:
        return ErrResponeModel("An error", "Invalid Request", response, 404)


# Delete user
@app.delete("/users/{id}")
async def delete_user(id: str, response: Response):
    try:
        deleted = await collection_users.delete_one({"_id": ObjectId(id)})
        if deleted.deleted_count == 1:
            return ResponeModel("", f"Already Delete user with id {id}", response, 200)
        else:
            response.status_code = 204
            return response.status_code
    except:
        return ErrResponeModel("An error", "Invalid Request", response, 404)
