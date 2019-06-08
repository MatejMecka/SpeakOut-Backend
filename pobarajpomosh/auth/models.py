"""
models.py

Responsible for all Models relating to Users and authentication

"""
from flask_login import UserMixin
from .. import db, login_manager
from passlib.apps import custom_app_context as pwd_context

@login_manager.user_loader
def get_user(ident):
    return User.query.get(int(ident))

class Role(db.Model):
    """
    Database Model for Representing User's role

    id(Integer, Unique and Primary Identifier for Roles)
    name(String, Unique, Names to Represent Roles)

    """
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return'<Role {}>'.format(self.name)


class User(UserMixin, db.Model):
    """
    Database Model for representing Users

    username the username
    password_hash the password hash
    role_id the Role the User is

    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    approved = db.Column(db.Integer, nullable=False, default=1)
    token = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    def hash_password(self, password):
        """
        Hash the Password
        :param: password: The supplied password
        """
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        """
        Verify if the password equals with the hash
        :param: password: The supplied password
        """
        return pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        return'<User {}>'.format(self.username)
