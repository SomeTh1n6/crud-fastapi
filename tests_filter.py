import pytest
from fastapi.testclient import TestClient
from main import app, Base, SessionLocal

client = TestClient(app)

# Фикстура для настройки базы данных перед каждым тестами
@pytest.fixture(scope="module")
def setup_database():
    # Создаем таблицы
    Base.metadata.create_all(bind=SessionLocal().bind)
    yield
    # Удаляем таблицы после тестов
    Base.metadata.drop_all(bind=SessionLocal().bind)

# Функция для настройки тестовых данных
def test_setup_items():
    items_data = [
        {"id": 1, "category": "electronics", "name": "Phone", "price": 200.0},
        {"id": 2, "category": "electronics", "name": "Laptop", "price": 1500.0},
        {"id": 3, "category": "furniture", "name": "Chair", "price": 75.0},
        {"id": 4, "category": "electronics", "name": "Tablet", "price": 300.0},
    ]
    for item_data in items_data:
        client.post("/items", json=item_data)
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == 4

# Тестирование фильтрации по цене
def test_filter_items(setup_database):
    response = client.get("/items/filter?min_price=100&max_price=400&sort=asc")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2
    assert items[0]["price"] == 200.0
    assert items[1]["price"] == 300.0

# Тестирование фильтрации, когда нет результатов
def test_filter_items_no_results(setup_database):
    response = client.get("/items/filter?min_price=1600&max_price=2000")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 0

# Тестирование фильтрации и сортировки по убыванию
def test_filter_items_descending(setup_database):
    response = client.get("/items/filter?min_price=0&max_price=2000&sort=desc")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 4
    assert items[0]["price"] == 1500.0
    assert items[1]["price"] == 300.0
    assert items[2]["price"] == 200.0
    assert items[3]["price"] == 75.0

if __name__ == "__main__":
    pytest.main()
