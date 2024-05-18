from pydantic import BaseModel, Field, constr
from typing import Optional, List

from app.models.maintenance import MaintenanceOrderStatus


class MaintenanceOrderBase(BaseModel):
    """
    Maintenance order base schema.

    Attributes:
    - vehicle_id (int): ID of the vehicle associated with the maintenance order.
    - service_type (str): Type of service for the maintenance order.
    - description (str): Description of the maintenance order.
    - status (str): Status of the maintenance order. Allowed values: "pending", "in_progress", "completed", "cancelled", "rejected"
    - mechanical_parts (List[str]): Mechanical parts of the maintenance
    """

    vehicle_id: int = Field(..., gt=0, example=1)
    service_type: str = Field(..., min_length=1, max_length=50, example="Oil Change")
    description: str = Field(..., min_length=1, example="Regular maintenance")
    status: MaintenanceOrderStatus = Field(..., example=MaintenanceOrderStatus.pending)
    mechanical_parts: List[constr(max_length=50)] = Field(
        example=["Engine oil filter", "Air filter", "Spark plugs"],
        description="List of mechanical parts involved in the maintenance."
    )

    class Config:
        orm_mode = True


class MaintenanceOrderCreate(MaintenanceOrderBase):
    """
    Maintenance order create schema based on MaintenanceOrderBase.
    """

    pass


class MaintenanceOrder(MaintenanceOrderBase):
    """
    Maintenance order schema.

    Extends:
    - MaintenanceOrderBase

    Additional Attributes:
    - id (int): ID of the maintenance order.

    Config:
    - orm_mode (bool): Enable ORM mode for this schema.
    """

    id: int

    class Config:
        orm_mode = True
