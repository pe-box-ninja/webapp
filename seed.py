from app import create_app, db
from app.models import (
    User,
    Package,
    Courier,
    Warehouse,
    ParcelLocker,
    Assignment,
    PackageStatus,
)
from faker import Faker
import random

from constants import MASTER_PASSWORD, MASTER_ADMIN_PASSWORD

fake = Faker("hu_HU")
VESZPREM_ADDRESSES = [
    "Egyetem utca 1., 8200 Veszprém",
    "Óváros tér 9., 8200 Veszprém",
    "Kossuth Lajos utca 21., 8200 Veszprém",
    "Wartha Vince utca 1., 8200 Veszprém",
    "Budapest út 47., 8200 Veszprém",
    "Cholnoky Jenő utca 22., 8200 Veszprém",
    "Haszkovó utca 18., 8200 Veszprém",
    "Jutasi út 59., 8200 Veszprém",
    "Március 15. utca 5., 8200 Veszprém",
    "Munkácsy Mihály utca 3., 8200 Veszprém",
    "Petőfi Sándor utca 8., 8500 Pápa",
    "Fő utca 12., 8500 Pápa",
    "Jókai Mór utca 5., 8500 Pápa",
    "Kossuth Lajos utca 27., 8100 Várpalota",
    "Szent István út 15., 8100 Várpalota",
    "Szabadság tér 1., 8220 Balatonalmádi",
    "Baross Gábor út 44., 8220 Balatonalmádi",
    "Petőfi Sándor utca 11., 8230 Balatonfüred",
    "Zákonyi Ferenc utca 2., 8230 Balatonfüred",
    "Kossuth Lajos utca 14., 8420 Zirc",
]


def get_random_address():
    return random.choice(VESZPREM_ADDRESSES)


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

    test_users = [
        User(username="raktar", email="warehouse@boxninja.com", role="warehouse"),
        User(username="futar", email="courier@boxninja.com", role="courier"),
        User(username="vendeg", email="guest@boxninja.com", role="guest"),
    ]
    for test_user in test_users:
        test_user.set_password(MASTER_PASSWORD)
        db.session.add(test_user)

    for _ in range(num_users):
        user = User(
            username=fake.user_name(), email=fake.email(), role=random.choice(roles)
        )
        user.set_password(MASTER_PASSWORD)
        db.session.add(user)
    db.session.commit()


def seed_packages(num_packages=100):
    statuses = PackageStatus.list()
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
            current_location="Veszprém",
            working_hours=f"{random.randint(6, 10)}:00 - {random.randint(14, 20)}:00",
            capacity=round(random.uniform(50, 200), 2),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year(),
        )
        db.session.add(courier)
    db.session.commit()


def seed_warehouses(num_warehouses=10):
    warehouse_addresses = [
        "Házgyári út 1., 8200 Veszprém",
        "Pápai út 34., 8200 Veszprém",
        "Ipar utca 2., 8100 Várpalota",
        "Gyártelep utca 1., 8500 Pápa",
        "Fűzfői út 15., 8220 Balatonalmádi",
        "Lóczy Lajos utca 30., 8230 Balatonfüred",
        "Ipari Park, 8420 Zirc",
    ]

    for address in warehouse_addresses[:num_warehouses]:
        warehouse = Warehouse(
            name=f"BoxNinja Raktár - {address.split(',')[1].strip()}",
            address=address,
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
            location="Veszprém",
            address=get_random_address(),
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

    used_warehouse = random.choice(warehouses).id
    used_parcel_locker = random.choice(lockers).id
    used_storage = used_warehouse if random.random() > 0.5 else used_parcel_locker

    for _ in range(num_assignments):
        assignment = Assignment(
            package_id=random.choice(packages).id,
            courier_id=random.choice(couriers).id,
            warehouse_id=(used_warehouse if used_storage == used_warehouse else None),
            parcel_locker_id=(
                used_parcel_locker if used_storage == used_parcel_locker else None
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
