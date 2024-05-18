from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.vehicle import VehicleCreate, Vehicle
from app.crud.vehicle import get_vehicle, get_vehicles, get_vehicle_by_license_plate, create_vehicle as db_create_vehicle

router = APIRouter(
    prefix="/vehicles",
    tags=["vehicles"],
    responses={404: {"description": "Not found"}},
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Vehicle, summary="Create a new vehicle", responses={
    201: {"description": "Vehicle created successfully"},
    400: {"description": "Vehicle already registered"},
    422: {"description": "Validation error"},
})
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    """
    Create a new vehicle.

    - **license_plate**: str - License plate of the vehicle (required, unique)
    - **model**: str - Model of the vehicle (required)
    - **year**: int - Year of manufacture (required)
    - **owner_id**: int - ID of the owner (required)
    """
    db_vehicle = get_vehicle_by_license_plate(db, license_plate=vehicle.license_plate)
    if db_vehicle:
        raise HTTPException(status_code=400, detail="Vehicle already registered")
    return db_create_vehicle(db=db, vehicle=vehicle)

@router.get("/{vehicle_id}", response_model=Vehicle, summary="Get a vehicle by ID", responses={
    200: {"description": "Vehicle found"},
    404: {"description": "Vehicle not found"},
})
def read_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a vehicle by its ID.

    - **vehicle_id**: int - ID of the vehicle to retrieve (required)
    """
    db_vehicle = get_vehicle(db, vehicle_id=vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

@router.get("/", response_model=list[Vehicle], summary="List vehicles", responses={
    200: {"description": "List of vehicles retrieved successfully"},
    422: {"description": "Validation error"},
})
def read_vehicles(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    """
    Retrieve a list of vehicles.

    - **skip**: int - Number of vehicles to skip (default is 0, must be non-negative)
    - **limit**: int - Maximum number of vehicles to return (default is 10, min is 1, max is 100)
    """
    vehicles = get_vehicles(db, skip=skip, limit=limit)
    return vehicles
