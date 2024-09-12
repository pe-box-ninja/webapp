from app import create_app, db
from app.models import (
    User,
    Package,
    Courier,
    Warehouse,
    ParcelLocker,
    Assignment
)

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Package': Package,
        'Courier': Courier,
        'Warehouse': Warehouse,
        'ParcelLocker': ParcelLocker,
        'Assignment': Assignment
    }

if __name__ == '__main__':
    app.run(debug=True)