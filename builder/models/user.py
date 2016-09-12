# coding: utf-8
import re
import random
import string
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from builder.exceptions import (InvalidPassword, InvalidUsername, InvalidEmail, PasswordMismatch, UserAlreadyExist,
                                UserNotFound, UserNotHasRole, InvalidCredentials)
from builder.models import Model, db


class User(Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'user'

    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    temporary = db.Column(db.Boolean(), default=True)
    active = db.Column(db.Boolean(), default=True)
    superuser = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.now())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    login_count = db.Column(db.Integer(), default=0)

    @classmethod
    def by_login(cls, login):
        """Search user by username or email"""
        if cls.verify_email(login):
            user = cls.query.filter(User.email == login).first()
        else:
            user = cls.query.filter(User.username == login).first()
        if not user:
            raise UserNotFound
        return user

    @classmethod
    def create(cls, username, email, password, confirm_password):
        """ Create a new user """
        if not cls.verify_username(username):
            raise InvalidUsername

        if not cls.verify_email(email):
            raise InvalidEmail

        if len(password) < 6:
            raise InvalidPassword

        if password != confirm_password:
            raise PasswordMismatch

        if not cls.valid_username_and_email(username, email):
            raise UserAlreadyExist

        user = User()
        user.username = username
        user.email = email
        user.password = cls.generate_password(password)
        user.save()
        db.session.commit()
        return user

    @classmethod
    def valid_username_and_email(cls, username, email):
        email_user = cls.query.filter(User.username == username).first()
        name_user = cls.query.filter(User.email == email).first()
        if name_user or email_user:
            return False
        return True

    def reload_stats(self):
        self.last_login_at = self.current_login_at
        self.current_login_at = datetime.now()
        self.login_count = self.login_count + 1
        self.save(commit=True)

    def change_password(self, old_password, password, confirm_password):
        """Change password of user"""
        if not self.validate_password(old_password):
            raise InvalidCredentials

        if len(password) < 6:
            raise InvalidPassword

        if password != confirm_password:
            raise PasswordMismatch

        self.password = self.generate_password(password)
        self.save()
        db.session.commit()

    def validate_password(self, password):
        """Used for validate hash password"""
        if check_password_hash(self.password, password):
            return True

    @staticmethod
    def random_password(size=12):
        """Create a string for password"""
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

    @staticmethod
    def verify_email(email):
        """Check if the email contains valid format"""
        if re.search(r'[\w.-]+@[\w.-]+.\w+', email):
            return True

    @staticmethod
    def verify_username(username):
        """Check length and if the username does not contains invalid chars"""
        if len(username) >= 3 and re.search(r'^[a-zA-Z0-9_.-]+$', username):
            return True

    @classmethod
    def generate_password(cls, password=None):
        """Create hash when password set or create a random password"""
        if not password:
            password = cls.random_password(12)
        return generate_password_hash(password)

    @property
    def roles(self):
        """Return all roles of this user"""
        roles = []
        for user_role in self.user_roles:
            roles.append(user_role.role)
        return roles

    def has_role(self, role):
        """Verify if this user have role"""
        if role in self.roles:
            return True

    def delete_all_roles(self):
        """Remove all roles of this user"""
        if not self.user_roles:
            raise UserNotHasRole

        for user_role in self.user_roles:
            user_role.delete(commit=True)
        db.session.commit()

    @property
    def is_superuser(self):
        return self.superuser

    @property
    def roles_available(self):
        from builder.models import Role
        roles = Role.query.filter(Role.active == True).all()
        available_roles = []
        for role in roles:
            if not self.has_role(role):
                available_roles.append(role)
        return available_roles
