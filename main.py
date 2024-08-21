import uvicorn
from fastapi import FastAPI, Query, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import declarative_base

# Настройка базы данных
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Определение модели базы данных
class ItemDB(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    name = Column(String)
    price = Column(Float)


# Создание таблиц
Base.metadata.create_all(bind=engine)

# FastAPI приложение
app = FastAPI()


class Item(BaseModel):
    id: int
    category: str
    name: str
    price: float


# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/items", response_model=List[Item])
async def read_items(db: Session = Depends(get_db)):
    items = db.query(ItemDB).all()
    return sorted(items, key=lambda item: item.id)


@app.get("/items/category/{category}", response_model=List[Item])
async def read_items_category(category: str, db: Session = Depends(get_db)):
    filtered_items = db.query(ItemDB).filter(ItemDB.category == category).all()
    return filtered_items


@app.get("/items/filter", response_model=List[Item])
async def read_items_filter(
        min_price: Optional[float] = Query(0.0),
        max_price: Optional[float] = Query(float('inf')),
        sort: Optional[str] = Query("asc"),
        db: Session = Depends(get_db)
):
    filtered_items = db.query(ItemDB).filter(ItemDB.price >= min_price, ItemDB.price <= max_price).all()

    if sort == "asc":
        return sorted(filtered_items, key=lambda item: item.price)
    elif sort == "desc":
        return sorted(filtered_items, key=lambda item: item.price, reverse=True)

    return filtered_items


@app.post("/items", response_model=Item)
async def create_item(item: Item, db: Session = Depends(get_db)):
    db_item = ItemDB(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item, db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in item.dict().items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
