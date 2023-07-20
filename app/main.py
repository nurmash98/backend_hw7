from fastapi import FastAPI, Response, Request, Depends, Form, HTTPException, Cookie
from pydantic import BaseModel
from jose import jwt
from typing import Annotated, List
from .flowers_repository import Flower, FlowersRepository
from .purchases_repository import Purchase, PurchasesRepository
from .users_repository import User, UsersRepository
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import json

app = FastAPI()
oauth2_schema = OAuth2PasswordBearer(tokenUrl = "token")
flowers_repo = FlowersRepository()
purchases_repo = PurchasesRepository()
users_repo = UsersRepository()

class SignUpRequest(BaseModel):
    username: str
    email: str 
    password: str 
    full_name: str | None = None

def encode_jwt(username: str) -> str:
    body = {"username" : username}
    token = jwt.encode(body, "Nurmash", "HS256")
    return token

def decode_jwt(token: str) -> str:
    data = jwt.decode(token, "Nurmash", "HS256")
    return data['username']

@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = form_data.username
    user = users_repo.get_by_username(username)
    if not user:
        raise HTTPException(status_code=400, detail="Such username not found")
    password = form_data.password
    if not password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    token = encode_jwt(username)
    return {"access_token": token, "token_type": "bearer"}



@app.post("/signup")    
def signup(user: SignUpRequest):
    new_user = User(username = user.username, email = user.email, password = user.password, full_name = user.full_name)
    users_repo.save(new_user)
    return Response("Successfully registered")

@app.get("/profile")
def get_profile(token: Annotated[str, Depends(oauth2_schema)]):
    username = decode_jwt(token)
    user = users_repo.get_by_username(username)
    return user

@app.get("/flowers")
def get_flowers(token: Annotated[str, Depends(oauth2_schema)]) -> List[Flower]:
    return flowers_repo.get_all()

class FlowerRequest(BaseModel):
    name: str 
    count: int 
    cost: int

@app.post("/flowers")
def post_flowers(flower: FlowerRequest, token: Annotated[str, Depends(oauth2_schema)]) -> int:
    flower = Flower(name = flower.name, count = flower.count, cost = flower.cost)
    flower_id = flowers_repo.save(flower)
    return flower_id


@app.get("/cart/items")
def get_cart_items(response: Response, cart: str = Cookie(default = "[]")):
    cart_json = json.loads(cart)
    flowers = flowers_repo.get_flowers_by_cart(cart_json)
    if not flowers:
        return Response("Not Valid Cart")
    return flowers

@app.post("/cart/items")
def post_cart_item(response: Response, flower_id: int = Form(), cart: str = Cookie(default = "[]")):
    response = Response("Added Flower")
    
    cart_json = json.loads(cart)
    if flower_id not in cart_json:
        cart_json.append(flower_id)
    
    new_cart = json.dumps(cart_json)
    response.set_cookie(key = "cart", value = new_cart)
    return response











