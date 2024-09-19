from app import create_app, db
from app.models import User, Package, Courier, Warehouse, ParcelLocker, Assignment
from faker import Faker
import random

from constants import MASTER_PASSWORD, MASTER_ADMIN_PASSWORD

fake = Faker()


def seed_users(num_users=50):
    roles = ["warehouse", "courier", "guest"]

    # Create the admin users
    admins = [
        User(username="admin_lidia", email="lidia.tovizi@gmail.com", role="admin"),
        User(username="admin_patrik", email="ballapatrik1999@gmail.com", role="admin"),
        User(username="admin_martin", email="martinkondor@gmail.com", role="admin"),
    ]
    for admin in admins:
        admin.set_password(MASTER_ADMIN_PASSWORD)
        db.session.add(admin)

    for _ in range(num_users):
        user = User(
            username=fake.user_name(), email=fake.email(), role=random.choice(roles)
        )
        user.set_password(MASTER_PASSWORD)
        db.session.add(user)
    db.session.commit()


def seed_packages(num_packages=100):
    statuses = ["függőben", "szállítás alatt", "kézbesítve", "visszaküldve"]
    for tracking_number in range(num_packages):
        package = Package(
            tracking_number=f"bn{tracking_number}",
            status=random.choice(statuses),
            weight=round(random.uniform(0.1, 20.0), 2),
            dimensions=f"{random.randint(1, 100)}x{random.randint(1, 100)}x{random.randint(1, 100)}",
            sender_address=fake.address(),
            recipient_address=fake.address(),
            delivery_deadline=fake.future_date(end_date="+30d"),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year(),
        )
        db.session.add(package)
    db.session.commit()


def seed_couriers(num_couriers=20):
    statuses = ["available", "on_delivery", "off_duty"]
    for _ in range(num_couriers):
        courier = Courier(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            status=random.choice(statuses),
            current_location=fake.city(),
            working_hours=f"{random.randint(6, 10)}:00 - {random.randint(14, 20)}:00",
            capacity=round(random.uniform(50, 200), 2),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year(),
        )
        db.session.add(courier)
    db.session.commit()


def seed_warehouses(num_warehouses=10):
    for _ in range(num_warehouses):
        warehouse = Warehouse(
            name=fake.company(),
            address=fake.address(),
            capacity=random.randint(1000, 10000),
            current_load=random.randint(0, 1000),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year(),
        )
        db.session.add(warehouse)
    db.session.commit()


def seed_parcel_lockers(num_lockers=30):
    for _ in range(num_lockers):
        locker = ParcelLocker(
            location=fake.city(),
            address=fake.address(),
            total_compartments=random.randint(20, 100),
            available_compartments=random.randint(0, 20),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year(),
        )
        db.session.add(locker)
    db.session.commit()


def seed_assignments(num_assignments=150):
    packages = Package.query.all()
    couriers = Courier.query.all()
    warehouses = Warehouse.query.all()
    lockers = ParcelLocker.query.all()
    statuses = ["assigned", "in_progress", "completed"]

    for _ in range(num_assignments):
        assignment = Assignment(
            package_id=random.choice(packages).id,
            courier_id=random.choice(couriers).id,
            warehouse_id=(
                random.choice(warehouses).id if random.random() > 0.5 else None
            ),
            parcel_locker_id=(
                random.choice(lockers).id if random.random() > 0.5 else None
            ),
            status=random.choice(statuses),
            assigned_at=fake.date_time_this_year(),
            completed_at=fake.date_time_this_year() if random.random() > 0.5 else None,
        )
        db.session.add(assignment)
    db.session.commit()


def clean_database():
    print("Cleaning database...")
    Assignment.query.delete()
    ParcelLocker.query.delete()
    Warehouse.query.delete()
    Courier.query.delete()
    Package.query.delete()
    User.query.delete()
    db.session.commit()
    print("Database cleaned successfully!")


def seed_database():
    clean_database()
    print("Seeding database...")
    seed_users()
    seed_packages()
    seed_couriers()
    seed_warehouses()
    seed_parcel_lockers()
    seed_assignments()
    print("Database seeded successfully!")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_database()
