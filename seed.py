from app import create_app, db
from app.models import (
    User,
    Package,
    Courier,
    Warehouse,
    ParcelLocker,
    Assignment,
    PackageStatus,
    CourierStatus,
    AssignmentStatus,
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

SENDER_ADDRESSES = [
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
]

RECIPIENT_ADDRESSES = [
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


def get_address_with_city():
    address = get_random_address()
    address_parts = address.split(" ")
    city = (
        address_parts[len(address.split(" ")) - 1]
        .strip()
        .replace("é", "")
        .replace("á", "")
        .replace("a", "")
        .replace("ö", "")
        .replace("ü", "")
        .upper()
    )
    return city, address


def get_random_address(type=None):
    if type == "sender":
        return random.choice(SENDER_ADDRESSES)
    elif type == "recipient":
        return random.choice(RECIPIENT_ADDRESSES)
    else:
        return random.choice(VESZPREM_ADDRESSES)


def get_random_status(no_done: bool = False):
    r = random.random()
    if no_done:
        if r < 0.1:
            return PackageStatus.RETURN
        elif r < 0.3:
            return PackageStatus.DELIVERED

    return PackageStatus.PENDING if random.random() > 0.5 else PackageStatus.IN_TRANSIT


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

    user = User.query.filter_by(username="futar").first()
    seed_courier_email = f"823z4e98hdf97shdf97hsd89fh3@boxninja_admin.com"

    courier = Courier(
        name="Seed Futár",
        email=seed_courier_email,
        phone=fake.phone_number(),
        status=(
            CourierStatus.AVAILABLE
            if random.random() > 0.2
            else CourierStatus.ON_DELIVERY
        ),
        current_location=get_address_with_city()[0],
        working_hours=f"{random.randint(6, 10)}:00 - {random.randint(14, 20)}:00",
        capacity=round(random.uniform(50, 200), 2),
    )
    db.session.add(courier)
    courier = Courier.query.filter_by(email=user.email).first()

    tracking_number = f"BN{fake.unique.random_int(min=1000, max=99999)}"
    package = Package(
        tracking_number=tracking_number,
        status=get_random_status(no_done=True),
        weight=round(random.uniform(0.1, 20.0), 2),
        dimensions=f"{random.randint(1, 100)}x{random.randint(1, 100)}x{random.randint(1, 100)}",
        sender_address=get_random_address("sender"),
        recipient_address=get_random_address("recipient"),
        delivery_deadline=fake.future_date(end_date="+30d"),
        created_at=fake.date_time_this_year(),
        updated_at=fake.date_time_this_year(),
    )
    db.session.add(package)
    package = Package.query.filter_by(tracking_number=tracking_number).first()

    assignment = Assignment(
        package_id=package.id,
        courier_id=user.id,
        status=str(AssignmentStatus.ASSIGNED),
        assigned_at=fake.date_time_this_year(),
    )
    db.session.add(assignment)

    for _ in range(num_users):
        username = f"{fake.user_name()}_{random.randint(1000, 9999)}"
        email = (
            f"{username}@{random.choice(['gmail', 'yahoo', 'hotmail', 'outlook'])}.com"
        )
        user = User(
            username=username,
            email=email,
            role=random.choice(roles),
        )
        user.set_password(MASTER_PASSWORD)
        db.session.add(user)

    db.session.commit()


def seed_packages(num_packages=500):
    for tracking_number in range(num_packages):
        package = Package(
            tracking_number=f"BN{fake.unique.random_int(min=1000, max=99999)}",
            status=get_random_status(no_done=False),
            weight=round(random.uniform(0.1, 20.0), 2),
            dimensions=f"{random.randint(1, 100)}x{random.randint(1, 100)}x{random.randint(1, 100)}",
            sender_address=get_random_address("sender"),
            recipient_address=get_random_address("recipient"),
            delivery_deadline=fake.future_date(end_date="+30d"),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year(),
        )
        db.session.add(package)
    db.session.commit()


def seed_couriers(num_couriers=20):
    statuses = CourierStatus.list()
    city2number = {}

    for _ in range(num_couriers):
        city, address = get_address_with_city()
        if city not in city2number:
            city2number[city] = 1
        else:
            city2number[city] += 1

        courier = Courier(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            status=random.choice(statuses),
            current_location=city,
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
    city2number = {}

    for address in warehouse_addresses[:num_warehouses]:
        address_parts = address.split(" ")
        city = (
            address_parts[len(address_parts) - 1]
            .strip()
            .replace("é", "")
            .replace("á", "")
            .replace("a", "")
            .replace("ö", "")
            .replace("ü", "")
            .upper()
        )
        if city not in city2number:
            city2number[city] = 1
        else:
            city2number[city] += 1
        city_id = f"{city}-{city2number[city]}"

        capacity = random.randint(10, 50)
        warehouse = Warehouse(
            name=f"BNR-{city_id}",
            address=address,
            capacity=capacity,
            current_load=0,  # Start with 0, will be updated in seed_assignments
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year(),
        )
        db.session.add(warehouse)
    db.session.commit()


def seed_parcel_lockers(num_lockers=10):
    city2number = {}

    for _ in range(num_lockers):
        city, address = get_address_with_city()
        if city not in city2number:
            city2number[city] = 1
        else:
            city2number[city] += 1

        total_compartments = random.randint(5, 20)
        locker = ParcelLocker(
            location=f"{city}-{city2number[city]}",
            address=address,
            total_compartments=total_compartments,
            available_compartments=total_compartments,
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year(),
        )
        db.session.add(locker)
    db.session.commit()


def seed_assignments(num_assignments=150):
    packages = Package.query.all()
    if not packages:
        print("No packages to assign!")
        return

    couriers = Courier.query.all()
    warehouses = Warehouse.query.all()
    lockers = ParcelLocker.query.all()
    statuses = AssignmentStatus.list()

    # Reset counters
    for warehouse in warehouses:
        warehouse.current_load = 0
    for locker in lockers:
        locker.available_compartments = locker.total_compartments

    # First ensure minimum packages for warehouses (10 each)
    for warehouse in warehouses:
        packages_needed = 10 + random.randint(0, warehouse.capacity - 1)
        packages_to_assign = [packages.pop() for _ in range(packages_needed)]

        for package in packages_to_assign:
            assignment = Assignment(
                package_id=package.id,
                courier_id=random.choice(couriers).id,
                warehouse_id=warehouse.id,
                parcel_locker_id=None,
                status=random.choice(statuses),
                assigned_at=fake.date_time_this_year(),
                completed_at=(
                    fake.date_time_this_year() if random.random() > 0.5 else None
                ),
            )
            db.session.add(assignment)
            warehouse.current_load += 1

    # Then ensure minimum packages for parcel lockers (10 each)
    for locker in lockers:
        packages_needed = min(10, locker.total_compartments)
        packages_to_assign = [packages.pop() for _ in range(packages_needed)]

        for package in packages_to_assign:
            assignment = Assignment(
                package_id=package.id,
                courier_id=random.choice(couriers).id,
                warehouse_id=None,
                parcel_locker_id=locker.id,
                status=random.choice(statuses),
                assigned_at=fake.date_time_this_year(),
                completed_at=(
                    fake.date_time_this_year() if random.random() > 0.5 else None
                ),
            )
            db.session.add(assignment)
            locker.available_compartments -= 1

    # Distribute remaining packages randomly between warehouses and lockers
    while packages:
        package = packages[0]
        if random.random() > 0.5:
            # Try to assign to a warehouse
            available_warehouses = [
                w for w in warehouses if w.current_load < w.capacity
            ]
            if available_warehouses:
                warehouse = random.choice(available_warehouses)
                assignment = Assignment(
                    package_id=package.id,
                    courier_id=random.choice(couriers).id,
                    warehouse_id=warehouse.id,
                    parcel_locker_id=None,
                    status=random.choice(statuses),
                    assigned_at=fake.date_time_this_year(),
                    completed_at=(
                        fake.date_time_this_year() if random.random() > 0.5 else None
                    ),
                )
                db.session.add(assignment)
                warehouse.current_load += 1
                packages.remove(package)
                continue

        # Try to assign to a parcel locker
        available_lockers = [l for l in lockers if l.available_compartments > 0]
        if available_lockers:
            locker = random.choice(available_lockers)
            assignment = Assignment(
                package_id=package.id,
                courier_id=random.choice(couriers).id,
                warehouse_id=None,
                parcel_locker_id=locker.id,
                status=random.choice(statuses),
                assigned_at=fake.date_time_this_year(),
                completed_at=(
                    fake.date_time_this_year() if random.random() > 0.5 else None
                ),
            )
            db.session.add(assignment)
            locker.available_compartments -= 1
            packages.remove(package)
        else:
            # If no space left in lockers, try warehouses again
            available_warehouses = [
                w for w in warehouses if w.current_load < w.capacity
            ]
            if available_warehouses:
                warehouse = random.choice(available_warehouses)
                assignment = Assignment(
                    package_id=package.id,
                    courier_id=random.choice(couriers).id,
                    warehouse_id=warehouse.id,
                    parcel_locker_id=None,
                    status=random.choice(statuses),
                    assigned_at=fake.date_time_this_year(),
                    completed_at=(
                        fake.date_time_this_year() if random.random() > 0.5 else None
                    ),
                )
                db.session.add(assignment)
                warehouse.current_load += 1
                packages.remove(package)
            else:
                # No space left anywhere
                break

    # Verify and update counters based on actual assignments
    for warehouse in warehouses:
        actual_count = Assignment.query.filter_by(
            warehouse_id=warehouse.id, completed_at=None
        ).count()
        warehouse.current_load = actual_count

    for locker in lockers:
        assigned_count = Assignment.query.filter_by(
            parcel_locker_id=locker.id, completed_at=None
        ).count()
        locker.available_compartments = locker.total_compartments - assigned_count

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
    print("Seeding users...")
    seed_users()
    print("Seeding packages...")
    seed_packages()
    print("Seeding couriers...")
    seed_couriers()
    print("Seeding warehouses...")
    seed_warehouses()
    print("Seeding parcel lockers...")
    seed_parcel_lockers()
    print("Seeding assignments...")
    seed_assignments()
    print("Database seeded successfully!")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_database()
