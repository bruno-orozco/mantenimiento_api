from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app.models.maintenance import MaintenanceOrder, MaintenanceOrderStatus
from app.models.vehicle import Vehicle
from app.schemas.maintenance import MaintenanceOrderCreate
from app.schemas.vehicle import VehicleCreate
from app.routers import vehicle, maintenance
from sqlalchemy import exc

app = FastAPI(
    title="Maintenance Order API",
    description="API for managing maintenance orders",
    version="0.1.0",
)

# Create the database tables
Base.metadata.create_all(bind=engine)


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to create initial data
def create_initial_data(db: Session):
    try:
        # Create initial vehicles if none exist
        if db.query(Vehicle).count() == 0:
            vehicle_data_1 = VehicleCreate(
                license_plate="ABC123",
                model="Toyota Corolla",
                year=2022,
                owner_id=1
            )
            db_vehicle_1 = Vehicle(**vehicle_data_1.dict())
            db.add(db_vehicle_1)

            vehicle_data_2 = VehicleCreate(
                license_plate="XYZ789",
                model="Honda Civic",
                year=2021,
                owner_id=2
            )
            db_vehicle_2 = Vehicle(**vehicle_data_2.dict())
            db.add(db_vehicle_2)

            vehicle_data_3 = VehicleCreate(
                license_plate="DEF456",
                model="Ford F-150",
                year=2019,
                owner_id=3
            )
            db_vehicle_3 = Vehicle(**vehicle_data_3.dict())
            db.add(db_vehicle_3)

            vehicle_data_4 = VehicleCreate(
                license_plate="GHI789",
                model="BMW X5",
                year=2020,
                owner_id=4
            )
            db_vehicle_4 = Vehicle(**vehicle_data_4.dict())
            db.add(db_vehicle_4)

            vehicle_data_5 = VehicleCreate(
                license_plate="JKL012",
                model="Tesla Model S",
                year=2023,
                owner_id=5
            )
            db_vehicle_5 = Vehicle(**vehicle_data_5.dict())
            db.add(db_vehicle_5)

            db.commit()

        # Create initial maintenance orders if none exist
        if db.query(MaintenanceOrder).count() == 0:
            order_data_1 = MaintenanceOrderCreate(
                description="Regular maintenance for Toyota Corolla",
                vehicle_id=1,
                service_type="Oil Change",
                status=MaintenanceOrderStatus.pending,
                mechanical_parts=["Engine oil filter", "Air filter"]
            )
            db_order_1 = MaintenanceOrder(**order_data_1.dict())
            db.add(db_order_1)

            order_data_2 = MaintenanceOrderCreate(
                description="Checkup for Honda Civic",
                vehicle_id=2,
                service_type="Inspection",
                status=MaintenanceOrderStatus.completed,
                mechanical_parts=["Brake pads check", "Fluid levels check"]
            )
            db_order_2 = MaintenanceOrder(**order_data_2.dict())
            db.add(db_order_2)

            order_data_3 = MaintenanceOrderCreate(
                description="Oil change and filter replacement for Ford F-150",
                vehicle_id=3,
                service_type="Oil Change",
                status=MaintenanceOrderStatus.in_progress,
                mechanical_parts=["Oil filter", "Fuel filter"]
            )
            db_order_3 = MaintenanceOrder(**order_data_3.dict())
            db.add(db_order_3)

            order_data_4 = MaintenanceOrderCreate(
                description="Tire replacement for BMW X5",
                vehicle_id=4,
                service_type="Tire Replacement",
                status=MaintenanceOrderStatus.pending,
                mechanical_parts=["Four new tires"]
            )
            db_order_4 = MaintenanceOrder(**order_data_4.dict())
            db.add(db_order_4)

            order_data_5 = MaintenanceOrderCreate(
                description="Brake check and service for Tesla Model S",
                vehicle_id=5,
                service_type="Brake Service",
                status=MaintenanceOrderStatus.completed,
                mechanical_parts=["Brake pads replacement", "Brake fluid flush"]
            )
            db_order_5 = MaintenanceOrder(**order_data_5.dict())
            db.add(db_order_5)

            db.commit()

    except exc.IntegrityError as e:
        db.rollback()
        print(f"Error creating initial data: {e}")
        raise HTTPException(status_code=500, detail="Error creating initial data")

# Run this function when the application starts
create_initial_data(SessionLocal())

# Include routers
app.include_router(vehicle.router)
app.include_router(maintenance.router)
