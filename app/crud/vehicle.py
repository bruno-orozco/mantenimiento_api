from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle as VehicleModel, Vehicle
from app.schemas.vehicle import VehicleCreate


def get_vehicle(db: Session, vehicle_id: int):
    """
    Retrieve a vehicle by its ID.

    Args:
    - db (Session): Database session dependency.
    - vehicle_id (int): ID of the vehicle to retrieve.

    Returns:
    - VehicleModel: The retrieved vehicle.
    """
    return db.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()


def get_vehicles(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieve a list of vehicles with pagination support.

    Args:
    - db (Session): Database session dependency.
    - skip (int): Number of records to skip.
    - limit (int): Maximum number of records to return.

    Returns:
    - List[VehicleModel]: A list of vehicles.
    """
    return db.query(VehicleModel).offset(skip).limit(limit).all()


def get_vehicle_by_license_plate(db: Session, license_plate: str):
    """
    Retrieve a vehicle by its license plate.

    Args:
    - db (Session): Database session dependency.
    - license_plate (str): License plate of the vehicle to retrieve.

    Returns:
    - Vehicle: The retrieved vehicle.
    """
    return db.query(Vehicle).filter(Vehicle.license_plate == license_plate).first()


def create_vehicle(db: Session, vehicle: VehicleCreate):
    """
    Create a new vehicle.

    Args:
    - db (Session): Database session dependency.
    - vehicle (VehicleCreate): Details of the vehicle to create.

    Returns:
    - VehicleModel: The created vehicle.
    """
    db_vehicle = VehicleModel(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle
