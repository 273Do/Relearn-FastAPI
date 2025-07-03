from fastapi import FastAPI
from typing import Union

app = FastAPI()

# 基本形


@app.get("/")
def root():
    return {"message": "Hello World"}


fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]

# クエリパラメータ


@app.get("/items/")
# パラメータは引数で定義する
def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


# パスパラメータ + クエリパラメータ
@app.get("/items/{item_id}")
# パスパラメータは同じ引数名で定義する
# Unionを使うことで、qがNoneもしくはstr型のどちらかを受け取ることができる
def read_item2(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
