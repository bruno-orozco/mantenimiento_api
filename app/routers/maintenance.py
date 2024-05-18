from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.crud.maintenance import (
    get_maintenance_order,
    get_maintenance_orders,
    create_maintenance_order as db_create_maintenance_order
)
from app.crud.vehicle import get_vehicle
from app.database import SessionLocal
from app.schemas.maintenance import MaintenanceOrder, MaintenanceOrderCreate

router = APIRouter(
    prefix="/maintenance-orders",
    tags=["maintenance_orders"],
    responses={404: {"description": "Not found"}},
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=MaintenanceOrder, summary="Create Maintenance Order")
def create_maintenance_order(
    order: MaintenanceOrderCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new maintenance order for a vehicle.

    - **vehicle_id**: int - ID of the vehicle associated with the maintenance order.
    - **service_type**: str - Type of service for the maintenance order.
    - **description**: str - Description of the maintenance order.
    - **status** (str): Status of the maintenance order. Allowed values: "pending", "in_progress", "completed", "cancelled", "rejected"
    - **mechanical_parts** (List[str]): Mechanical parts of the maintenance

    """
    # Check if the vehicle_id exists
    vehicle = get_vehicle(db, order.vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail=f"Vehicle with id {order.vehicle_id} not found")

    # Create the maintenance order only if the vehicle_id exists
    db_order = db_create_maintenance_order(db=db, order=order)
    return db_order

@router.get("/{order_id}", response_model=MaintenanceOrder, summary="Get Maintenance Order")
def read_maintenance_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific maintenance order by its ID.

    - **order_id**: The ID of the maintenance order to retrieve.

    Returns the maintenance order.
    """
    db_order = get_maintenance_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.get("/", response_model=List[MaintenanceOrder], summary="List Maintenance Orders")
def read_maintenance_orders(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    List all maintenance orders with pagination support.

    - **skip**: Number of records to skip.
    - **limit**: Maximum number of records to return.

    Returns a list of maintenance orders.
    """
    orders = get_maintenance_orders(db, skip=skip, limit=limit)
    return orders
