from pydantic import BaseModel, Field


class VehicleBase(BaseModel):
    """
    Vehicle base schema.

    Attributes:
    - license_plate (str): License plate of the vehicle.
    - model (str): Model of the vehicle.
    - year (int): Year of manufacture of the vehicle.
    - owner_id (int): ID of the owner of the vehicle.
    """

    license_plate: str = Field(..., min_length=1, max_length=10, example="ABC123")
    model: str = Field(..., min_length=1, max_length=50, example="Toyota Corolla")
    year: int = Field(..., ge=1886, le=2100, example=2022)
    owner_id: int = Field(..., ge=1, example=1)


class VehicleCreate(VehicleBase):
    """
    Vehicle create schema based on VehicleBase.
    """

    pass


class Vehicle(VehicleBase):
    """
    Vehicle schema.

    Extends:
    - VehicleBase

    Additional Attributes:
    - id (int): ID of the vehicle.

    Config:
    - orm_mode (bool): Enable ORM mode for this schema.
    """

    id: int

    class Config:
        orm_mode = True
