from fastapi.testclient import TestClient
from app.main import app
import pytest
from faker import Faker

client = TestClient(app)
fake = Faker()

@pytest.fixture(scope="module")
def test_client():
    """
    Fixture to provide a test client configured with the application.
    """
    with TestClient(app) as c:
        yield c

def create_test_maintenance_order():
    """
    Helper function to create test data for maintenance orders.
    """
    fake = Faker()
    order_data = {
        "vehicle_id": 1,
        "service_type": fake.word(),
        "description": fake.sentence(),
        "status": "pending",
        "mechanical_parts": [
            fake.word(),
            fake.word(),
            fake.word()
        ]
    }
    return order_data

def test_create_maintenance_order(test_client):
    """
    Unit test to create a maintenance order.
    """
    order_data = create_test_maintenance_order()
    response = test_client.post("/maintenance-orders/", json=order_data)

    assert response.status_code == 200
    assert response.json()["description"] == order_data["description"]
    assert response.json()["vehicle_id"] == order_data["vehicle_id"]
    assert response.json()["service_type"] == order_data["service_type"]

    # Validate data types
    assert isinstance(response.json()["id"], int)
    assert isinstance(response.json()["description"], str)
    assert isinstance(response.json()["vehicle_id"], int)
    assert isinstance(response.json()["service_type"], str)

def test_read_maintenance_order(test_client):
    """
    Unit test to read a maintenance order by its ID.
    """
    # Create a test maintenance order first
    order_data = create_test_maintenance_order()
    response = test_client.post("/maintenance-orders/", json=order_data)
    order_id = response.json()["id"]

    # Then read the maintenance order
    response = test_client.get(f"/maintenance-orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["id"] == order_id
    assert response.json()["description"] == order_data["description"]
    assert response.json()["vehicle_id"] == order_data["vehicle_id"]
    assert response.json()["service_type"] == order_data["service_type"]

    # Validate data types
    assert isinstance(response.json()["id"], int)
    assert isinstance(response.json()["description"], str)
    assert isinstance(response.json()["vehicle_id"], int)
    assert isinstance(response.json()["service_type"], str)

def test_read_maintenance_orders(test_client):
    """
    Unit test to list all maintenance orders.
    """
    # Create some test maintenance orders
    for _ in range(5):
        order_data = create_test_maintenance_order()
        test_client.post("/maintenance-orders/", json=order_data)

    # Then read the maintenance orders
    response = test_client.get("/maintenance-orders/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for order in response.json():
        assert "id" in order
        assert isinstance(order["id"], int)
        assert isinstance(order["description"], str)
        assert isinstance(order["vehicle_id"], int)
        assert isinstance(order["service_type"], str)

def test_read_maintenance_orders_with_pagination(test_client):
    """
    Unit test to list maintenance orders with pagination.
    """
    # Create some test maintenance orders
    for _ in range(15):
        order_data = create_test_maintenance_order()
        test_client.post("/maintenance-orders/", json=order_data)

    # Then read maintenance orders with pagination
    response = test_client.get("/maintenance-orders/?skip=0&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Ensure 10 records are returned
    assert len(response.json()) == 10
    for order in response.json():
        assert "id" in order
        assert isinstance(order["id"], int)
        assert isinstance(order["description"], str)
        assert isinstance(order["vehicle_id"], int)
        assert isinstance(order["service_type"], str)
