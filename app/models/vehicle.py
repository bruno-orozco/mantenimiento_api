from sqlalchemy import Column, Integer, String
from app.database import Base


class Vehicle(Base):
    """
    Vehicle model represents a vehicle.

    Attributes:
    - id (int): Primary key ID of the vehicle.
    - license_plate (str): License plate number of the vehicle (unique).
    - make (str): Make or manufacturer of the vehicle.
    - model (str): Model name of the vehicle.
    - year (int): Year of manufacture of the vehicle.
    - owner_id (int): ID of the owner of the vehicle.
    """

    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String, unique=True, index=True)
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    owner_id = Column(Integer)
