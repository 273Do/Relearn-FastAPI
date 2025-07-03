from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel

app = FastAPI()

# 自動でopenapiのドキュメントを生成してくれる
# get基本形


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

# リクエストボディ


class Item(BaseModel):
    name: str
    description: Union[str, None] = None  # 同様にNoneをつけることでオプショナルにできる
    price: float
    tax: Union[float, None] = None

# post基本形


@app.post("/items/")
# Item型の引数を受け取ることで、リクエストボディを自動的に検証してくれる
def create_item(item: Item):
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})  # 辞書に値を追加する
    return item_dict

# リクエストボディ + パスパラメータ + クエリパラメータ


@app.put("/items/{item_id}")
# パラメータがパスで宣言されている場合は、優先的にパスパラメータとして扱われます。
# パラメータが単数型(int、float、str、bool など)の場合はクエリパラメータとして解釈されます。
# パラメータが Pydantic モデル型で宣言された場合、リクエストボディとして解釈されます。
def update_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
