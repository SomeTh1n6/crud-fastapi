import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    price: float

items = []

@app.get("/items", response_model=List[Item])
async def read_items():
    return items

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    items.append(item)
    return item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    for index, existing_item in enumerate(items):
        if existing_item.id == item_id:
            items[index] = item
            return item
    return {"error": "Item not found"}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    for index, existing_item in enumerate(items):
        if existing_item.id == item_id:
            del items[index]
            return {"message": "Item deleted"}
    return {"error": "Item not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)