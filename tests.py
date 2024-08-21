import pytest
from fastapi.testclient import TestClient
from main import app, Base, SessionLocal

client = TestClient(app)

# Фикстура для настройки базы данных перед тестами
@pytest.fixture(scope="module")
def setup_database():
    # Создаем таблицы
    Base.metadata.create_all(bind=SessionLocal().bind)
    yield
    # Удаляем таблицы после тестов
    Base.metadata.drop_all(bind=SessionLocal().bind)

# Тестирование создания элемента
def test_create_item(setup_database):
    response = client.post("/items", json={"id": 1, "category": "electronics", "name": "Test Item", "price": 10.0})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "category": "electronics", "name": "Test Item", "price": 10.0}

# Тестирование чтения всех элементов
def test_read_items(setup_database):
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == 1

# Тестирование фильтрации по категории
def test_read_items_category(setup_database):
    response = client.get("/items/category/electronics")
    assert response.status_code == 200
    assert len(response.json()) == 1

# Тестирование обновления элемента
def test_update_item(setup_database):
    response = client.put("/items/1", json={"id": 1, "category": "electronics", "name": "Updated Item", "price": 15.0})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "category": "electronics", "name": "Updated Item", "price": 15.0}

# Тестирование чтения обновленного элемента
def test_read_updated_item(setup_database):
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json()[0] == {"id": 1, "category": "electronics", "name": "Updated Item", "price": 15.0}

# Тестирование удаления элемента
def test_delete_item(setup_database):
    response = client.delete("/items/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted"}

# Тестирование чтения элементов после удаления
def test_read_items_after_deletion(setup_database):
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == 0

# Тестирование создания нескольких элементов
def test_create_multiple_items(setup_database):
    items_data = [
        {"id": 2, "category": "electronics", "name": "Test Item 2", "price": 20.0},
        {"id": 3, "category": "furniture", "name": "Test Item 3", "price": 30.0},
    ]

    for item_data in items_data:
        response = client.post("/items", json=item_data)
        assert response.status_code == 200
        assert response.json() == item_data

# Тестирование фильтрации по категории "furniture"
def test_read_items_category_furniture(setup_database):
    response = client.get("/items/category/furniture")
    assert response.status_code == 200
    assert len(response.json()) == 1

if __name__ == "__main__":
    pytest.main()
