import uvicorn
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Item(BaseModel):
    id: int
    category: str
    name: str
    price: float

items = []

@app.get("/items", response_model=List[Item])
async def read_items():
    return sorted(items, key=lambda item: item.id)

@app.get("/items/category/{category}", response_model=List[Item])
async def read_items_category(category):
    filtered_items = [item for item in items if item.category == category]
    return filtered_items

@app.get("/items/filter", response_model=List[Item])
async def read_items_filter(
        min_price: Optional[float] = Query(0.0),
        max_price: Optional[float] = Query(float('inf')),
        sort: Optional[str] = Query("asc")
):
    print(f"Filtering items with min_price: {min_price}, max_price: {max_price}, sort: {sort}")

    # Фильтрация по цене
    filtered_items = [
        item for item in items if (item.price >= min_price) and (item.price <= max_price)
    ]

    # Сортировка
    if sort == "asc":
        return sorted(filtered_items, key=lambda item: item.price)
    elif sort == "desc":
        return sorted(filtered_items, key=lambda item: item.price, reverse=True)

    return filtered_items

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    for existing_item in items:
        if existing_item.id == item.id:
            raise HTTPException(status_code=400, detail="Item with this ID already exists.")

    items.append(item)
    return item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id == item.id:
        for index, existing_item in enumerate(items):
            if existing_item.id == item_id:
                items[index] = item
                return item
        return {"error": "Item not found"}
    raise HTTPException(status_code=400, detail="IDs are different")


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    for index, existing_item in enumerate(items):
        if existing_item.id == item_id:
            del items[index]
            return {"message": "Item deleted"}
    return {"error": "Item not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)