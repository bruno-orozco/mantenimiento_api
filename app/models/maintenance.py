from sqlalchemy import Column, Integer, String, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum as PyEnum


class MaintenanceOrderStatus(str, PyEnum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"
    rejected = "rejected"


class MaintenanceOrder(Base):
    """
    MaintenanceOrder model represents a maintenance order for a vehicle.

    Attributes:
    - id (int): Primary key ID of the maintenance order.
    - vehicle_id (int): Foreign key ID referencing the associated vehicle.
    - service_type (str): Type of service for the maintenance.
    - description (str): Description of the maintenance order.
    - status (str): Current status of the maintenance order.
    - mechanical_parts (JSON): JSON field to store mechanical parts involved in the maintenance order.
    """

    __tablename__ = "maintenance_orders"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    service_type = Column(String)
    description = Column(String)
    status = Column(Enum(MaintenanceOrderStatus), nullable=False)  # Using Enum for choices
    mechanical_parts = Column(JSON)

    vehicle = relationship("Vehicle")
