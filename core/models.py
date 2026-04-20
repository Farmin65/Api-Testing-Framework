from pydantic import BaseModel, Field, HttpUrl, EmailStr, ConfigDict
from typing import Optional, List


class Geo(BaseModel):
    lat: str
    lng: str


class Address(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo


class Company(BaseModel):
    name: str
    catchPhrase: str
    bs: str


class User(BaseModel):
    model_config = ConfigDict(extra='allow')

    id: int
    name: str
    username: str
    email: EmailStr
    address: Address
    phone: str
    website: str  # Changed from HttpUrl to str
    company: Company


class Post(BaseModel):
    model_config = ConfigDict(extra='allow')

    userId: int = Field(..., ge=1)
    id: int
    title: str
    body: str


class Comment(BaseModel):
    model_config = ConfigDict(extra='allow')

    postId: int
    id: int
    name: str
    email: EmailStr
    body: str