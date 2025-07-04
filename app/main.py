# チュートリアル：https://fastapi.tiangolo.com/ja/tutorial/

from typing import Union, Annotated, Literal
from fastapi import FastAPI, Query, Body
from pydantic import BaseModel, Field

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

# クエリパラメータのバリデーションは以下のように設定できる


@app.get("/items/")
async def read_items(
    q: Union[str, None] = Query(
        default=None, min_length=3, max_length=50, pattern="^fixedquery$",
        title="openapiのタイトル",
        description="説明をここに書ける",
    ),  # デフォルトを指定しなければ必須になる
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# クエリパラメータにPydanticモデルを使用できる


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items2/")
def read_items2(filter_query: Annotated[FilterParams, Query(default={})]):
    return filter_query

# パスパラメータのバリデーションはfastapiからPathをインポート
# クエリパラメータと同様に設定できる

# ボディのバリデーションはPydanticモデルを使用して行う


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


@app.put("/items2/{item_id}")
def update_item2(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(gt=0),
    q: Union[str, None] = None,
):
    results = {"item_id": item_id, "item": item,
               "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results


class Item(BaseModel):
    name: str
    # Fieldを使うことで、OpenAPIのドキュメントにタイトルや説明を追加できる
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(
        gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None


@app.put("/items/{item_id}")
def update_item3(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
