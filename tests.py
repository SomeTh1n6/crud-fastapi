import pytest
from fastapi.testclient import TestClient
from main import app, Item  # Предполагается, что ваш код находится в файле main.py

client = TestClient(app)

# Тестирование создания элемента
def test_create_item():
    response = client.post("/items", json={"id": 1, "name": "Test Item", "price": 10.0})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test Item", "price": 10.0}

# Тестирование чтения элементов
def test_read_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Test Item", "price": 10.0}]

# Тестирование обновления элемента
def test_update_item():
    response = client.put("/items/1", json={"id": 1, "name": "Updated Item", "price": 15.0})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Updated Item", "price": 15.0}

# Тестирование чтения обновленного элемента
def test_read_updated_item():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Updated Item", "price": 15.0}]

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

if __name__ == "__main__":
    pytest.main()