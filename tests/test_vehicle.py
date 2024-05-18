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

def test_create_vehicle(test_client):
    """
    Unit test to create a new vehicle.
    """
    vehicle_data = {
        "license_plate": fake.lexify(text="???###"),
        "model": fake.word(),
        "year": fake.random_int(min=1980, max=2023),
        "owner_id": fake.random_int(min=1, max=100)
    }
    response = test_client.post("/vehicles/", json=vehicle_data)

    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["license_plate"] == vehicle_data["license_plate"]
    assert response.json()["model"] == vehicle_data["model"]
    assert response.json()["year"] == vehicle_data["year"]
    assert response.json()["owner_id"] == vehicle_data["owner_id"]

    # Validating data types
    assert isinstance(response.json()["id"], int)
    assert isinstance(response.json()["license_plate"], str)
    assert isinstance(response.json()["model"], str)
    assert isinstance(response.json()["year"], int)
    assert isinstance(response.json()["owner_id"], int)

def test_create_vehicle_already_registered(test_client):
    """
    Unit test to handle scenario where vehicle is already registered.
    """
    # Assuming the vehicle was already created in the previous test
    vehicle_data = {
        "license_plate": "ABC123",
        "model": "Test Model",
        "year": 2020,
        "owner_id": 1
    }
    response = test_client.post("/vehicles/", json=vehicle_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Vehicle already registered"}

def test_read_vehicle(test_client):
    """
    Unit test to read a vehicle by its ID.
    """
    response = test_client.get("/vehicles/1")
    assert response.status_code == 200
    assert "id" in response.json()
    assert isinstance(response.json()["id"], int)
    assert isinstance(response.json()["license_plate"], str)
    assert isinstance(response.json()["model"], str)
    assert isinstance(response.json()["year"], int)
    assert isinstance(response.json()["owner_id"], int)

def test_read_vehicle_not_found(test_client):
    """
    Unit test to handle scenario where the vehicle is not found.
    """
    response = test_client.get("/vehicles/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Vehicle not found"}

def test_read_vehicles(test_client):
    """
    Unit test to list all vehicles.
    """
    response = test_client.get("/vehicles/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for vehicle in response.json():
        assert "id" in vehicle
        assert isinstance(vehicle["id"], int)
        assert isinstance(vehicle["license_plate"], str)
        assert isinstance(vehicle["model"], str)
        assert isinstance(vehicle["year"], int)
        assert isinstance(vehicle["owner_id"], int)

def test_read_vehicles_with_pagination(test_client):
    """
    Unit test to list vehicles with pagination.
    """
    response = test_client.get("/vehicles/?skip=0&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for vehicle in response.json():
        assert "id" in vehicle
        assert isinstance(vehicle["id"], int)
        assert isinstance(vehicle["license_plate"], str)
        assert isinstance(vehicle["model"], str)
        assert isinstance(vehicle["year"], int)
        assert isinstance(vehicle["owner_id"], int)
