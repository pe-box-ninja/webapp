from app import create_app
from app.models import (
    Warehouse,
    ParcelLocker,
)


def db_test():
    warehouses = Warehouse.query.all()
    for warehouse in warehouses:
        print("-" * 10)
        print(str(warehouse))

    lockers = ParcelLocker.query.all()
    for locker in lockers:
        print("-" * 10)
        print(str(locker))


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db_test()
