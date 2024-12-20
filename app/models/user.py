from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(
        db.Enum("admin", "warehouse", "courier", "guest", name="user_role")
    )
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == "admin"

    def is_courier(self):
        return self.role == "courier"

    def is_warehouse(self):
        return self.role == "warehouse"

    def is_guest(self):
        return self.role == "guest"
    
    def user_roles(self):
        list=["admin", "warehouse", "courier", "guest"]
        return list


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
