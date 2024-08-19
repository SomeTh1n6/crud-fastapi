import pytest
from fastapi.testclient import TestClient
from main import app, Item

client = TestClient(app)

def setup_items():
    items_data = [
        {"id":1, "category":"electronics", "name":"Phone", "price":200.0},
        {"id":2, "category":"electronics", "name":"Laptop", "price":1500.0},
        {"id":3, "category":"furniture", "name":"Chair", "price":75.0},
        {"id":4, "category":"electronics", "name":"Tablet", "price":300.0},
    ]
    for item_data in items_data:
        client.post("/items", json=item_data)


def test_filter_items():
    setup_items()
    # Тестирование фильтрации по цене
    response = client.get("/items/filter?min_price=100&max_price=400&sort=asc")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2
    assert items[0]["price"] == 200.0  # Phone
    assert items[1]["price"] == 300.0  # Tablet

def test_filter_items_no_results():
    setup_items()
    # Тестирование фильтрации, когда нет результатов
    response = client.get("/items/filter?min_price=1600&max_price=2000")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 0

def test_filter_items_descending():
    setup_items()
    # Тестирование фильтрации и сортировки по убыванию
    response = client.get("/items/filter?min_price=0&max_price=2000&sort=desc")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 4
    assert items[0]["price"] == 1500.0  # Laptop
    assert items[1]["price"] == 300.0  # Tablet
    assert items[2]["price"] == 200.0  # Phone
    assert items[3]["price"] == 75.0   # Chair

if __name__ == "__main__":
    pytest.main()