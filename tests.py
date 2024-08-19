import pytest
from fastapi.testclient import TestClient
from main import app, Item  # Предполагается, что ваш код находится в файле main.py

client = TestClient(app)

# Тестирование создания элемента
def test_create_item():
        response = client.post("/items", json={"id": 1, "category": "electronics", "name": "Test Item", "price": 10.0})
        assert response.status_code == 200
        assert response.json() == {"id": 1, "category": "electronics", "name": "Test Item", "price": 10.0}

# Тестирование чтения всех элементов
def test_read_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "category": "electronics", "name": "Test Item", "price": 10.0}]

# Тестирование фильтрации по категории
def test_read_items_category():
    response = client.get("/items/category/electronics")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "category": "electronics", "name": "Test Item", "price": 10.0}]

# Тестирование обновления элемента
def test_update_item():
    response = client.put("/items/1", json={"id": 1, "category": "electronics", "name": "Updated Item", "price": 15.0})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "category": "electronics", "name": "Updated Item", "price": 15.0}

# Тестирование чтения обновленного элемента
def test_read_updated_item():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "category": "electronics", "name": "Updated Item", "price": 15.0}]

# Тестирование удаления элемента
def test_delete_item():
    response = client.delete("/items/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted"}

# Тестирование чтения элементов после удаления
def test_read_items_after_deletion():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []

# Тестирование создания нескольких элементов
def test_create_multiple_items():
    # Создаем три элемента с разными категориями
    items_data = [
        {"id": 1, "category": "electronics", "name": "Test Item 1", "price": 10.0},
        {"id": 2, "category": "furniture", "name": "Test Item 2", "price": 20.0},
        {"id": 3, "category": "electronics", "name": "Test Item 3", "price": 30.0},
    ]

    for item_data in items_data:
        response = client.post("/items", json=item_data)
        assert response.status_code == 200
        assert response.json() == item_data

# Тестирование чтения всех элементов
def test_read_multiple_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == 3  # Проверяем, что три элемента были добавлены

# Тестирование фильтрации по категории "electronics"
def test_read_items_category_electronics():
    response = client.get("/items/category/electronics")
    assert response.status_code == 200
    assert len(response.json()) == 2  # Должно быть два элемента в категории "electronics"
    assert response.json() == [
        {"id": 1, "category": "electronics", "name": "Test Item 1", "price": 10.0},
        {"id": 3, "category": "electronics", "name": "Test Item 3", "price": 30.0},
    ]

# Тестирование фильтрации по категории "furniture"
def test_read_items_category_furniture():
    response = client.get("/items/category/furniture")
    assert response.status_code == 200
    assert len(response.json()) == 1  # Должен быть один элемент в категории "furniture"
    assert response.json() == [
        {"id": 2, "category": "furniture", "name": "Test Item 2", "price": 20.0},
    ]

if __name__ == "__main__":
    pytest.main()