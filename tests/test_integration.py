from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine, Base
from app.models.maintenance import MaintenanceOrder, MaintenanceOrderStatus
from app.models.vehicle import Vehicle
from app.schemas.maintenance import MaintenanceOrderCreate
from app.schemas.vehicle import VehicleCreate
from sqlalchemy.orm import Session
import pytest
from faker import Faker

# Set up test database
Base.metadata.create_all(bind=engine)


# Override the database dependency to use the test database
@pytest.fixture(scope="module")
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a test client
client = TestClient(app)
fake = Faker()


# Fixture to provide a test session
@pytest.fixture(scope="module")
def test_session():
    with SessionLocal() as session:
        yield session


def create_test_maintenance_order(db: Session):
    fake = Faker()
    order_data = MaintenanceOrderCreate(
        description=fake.sentence(),
        vehicle_id=1,
        service_type=fake.word(),
        status=MaintenanceOrderStatus.pending,
        mechanical_parts=[fake.word(), fake.word(), fake.word()]
    )
    return order_data


def create_test_vehicle(db: Session):
    fake = Faker()
    vehicle_data = VehicleCreate(
        license_plate=fake.lexify(text="???###"),
        model=fake.word(),
        year=fake.random_int(min=1980, max=2023),
        owner_id=fake.random_int(min=1, max=100)
    )
    return vehicle_data


# Integration tests for maintenance orders
def test_create_and_read_maintenance_order(test_session):
    order_data = create_test_maintenance_order(test_session)

    # Create maintenance order
    response = client.post("/maintenance-orders/", json=order_data.dict())
    assert response.status_code == 200
    created_order = MaintenanceOrder(**response.json())

    # Read maintenance order
    response = client.get(f"/maintenance-orders/{created_order.id}")
    assert response.status_code == 200
    assert response.json()["id"] == created_order.id
    assert response.json()["description"] == created_order.description


def test_list_maintenance_orders(test_session):
    # Create multiple maintenance orders
    for _ in range(5):
        order_data = create_test_maintenance_order(test_session)
        client.post("/maintenance-orders/", json=order_data.dict())

    # List maintenance orders
    response = client.get("/maintenance-orders/")
    assert response.status_code == 200


# Integration tests for vehicles
def test_create_and_read_vehicle(test_session):
    vehicle_data = create_test_vehicle(test_session)

    # Create vehicle
    response = client.post("/vehicles/", json=vehicle_data.dict())
    assert response.status_code == 200
    created_vehicle = Vehicle(**response.json())

    # Read vehicle
    response = client.get(f"/vehicles/{created_vehicle.id}")
    assert response.status_code == 200
    assert response.json()["id"] == created_vehicle.id
    assert response.json()["license_plate"] == created_vehicle.license_plate


def test_list_vehicles(test_session):
    # Create multiple vehicles
    for _ in range(5):
        vehicle_data = create_test_vehicle(test_session)
        client.post("/vehicles/", json=vehicle_data.dict())

    # List vehicles
    response = client.get("/vehicles/")
    assert response.status_code == 200