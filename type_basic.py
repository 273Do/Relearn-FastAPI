# from typing import Union

# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

# def get_full_name(first_name: str, last_name: str):
#     full_name = first_name.title() + " " + last_name.title()
#     return full_name

# print(get_full_name("john", "doe"))

# def get_name_with_age(name: str, age: int):
#     name_with_age = name + " is this old: " + str(age)
#     return name_with_age

# from typing import List


# def process_items(items: List[str]):
#     for item in items:
#         print(item)

# class Person:
#     def __init__(self, name: str):
#         self.name = name


# def get_person_name(one_person: Person):
#     return one_person.name

# from datetime import datetime
# from typing import List, Union

# from pydantic import BaseModel


# class User(BaseModel):
#     id: int
#     name: str = "John Doe"
#     signup_ts: Union[datetime, None] = None
#     friends: List[int] = []


# external_data = {
#     "id": "123",
#     "signup_ts": "2017-06-01 12:22",
#     "friends": [1, "2", b"3"],
# }
# user = User(**external_data)
# print(user)
# # > User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]
# print(user.id)
# # > 123
