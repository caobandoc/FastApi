#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    age: int = Field(
        ...,
        gt=0,
        le=99
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    
    class Config:
        schema_extra = {
            "example":{
                "first_name":"Carlos",
                "last_name":"Obando Casiano",
                "age":21,
                "hair_color":"black",
                "is_married":False
            }
        }
    
    
class Location(BaseModel):
    city: str
    state: str
    country: str

@app.get("/")
def home():
    return {"Hello": "Hello World"}

# Request and Response body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's requeried"
        )
):
    return {name: age}

# Validaciones: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Persone ID",
        description="This is the person ID. It's requeried and greater than 0"
        )
):
    return {person_id:"It exists¡"}

# Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID. It's requeried and greater than 0",
        gt=0
        ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    return {
        "person": person,
        "location": location
    }