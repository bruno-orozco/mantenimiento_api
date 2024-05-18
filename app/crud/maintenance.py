from sqlalchemy.orm import Session
from app.models.maintenance import MaintenanceOrder
from app.schemas.maintenance import MaintenanceOrderCreate


def get_maintenance_order(db: Session, order_id: int):
    """
    Retrieve a maintenance order by its ID.

    Args:
    - db (Session): Database session dependency.
    - order_id (int): ID of the maintenance order to retrieve.

    Returns:
    - MaintenanceOrder: The retrieved maintenance order.
    """
    return db.query(MaintenanceOrder).filter(MaintenanceOrder.id == order_id).first()


def get_maintenance_orders(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieve a list of maintenance orders with pagination support.

    Args:
    - db (Session): Database session dependency.
    - skip (int): Number of records to skip.
    - limit (int): Maximum number of records to return.

    Returns:
    - List[MaintenanceOrder]: A list of maintenance orders.
    """
    return db.query(MaintenanceOrder).offset(skip).limit(limit).all()


def create_maintenance_order(db: Session, order: MaintenanceOrderCreate):
    """
    Create a new maintenance order.

    Args:
    - db (Session): Database session dependency.
    - order (MaintenanceOrderCreate): Details of the maintenance order to create.

    Returns:
    - MaintenanceOrder: The created maintenance order.
    """
    db_order = MaintenanceOrder(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
