# coding: utf-8
import re
import random
import string
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from builder.exceptions import (InvalidPassword, InvalidUsername, InvalidEmail, PasswordMismatch, UserAlreadyExist,
                                UserNotFound, UserNotHasRole, InvalidCredentials, UserAlreadyInRole)
from builder.models import Model, db
from builder.models.role import Role


class User(Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'user'

    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.now())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    login_count = db.Column(db.Integer(), default=0)

    @property
    def superuser(self):
        return self.search_user_role('superuser')

    @property
    def admin(self):
        return self.search_user_role('admin')

    @property
    def client(self):
        return self.search_user_role('client')

    @property
    def reviewer(self):
        return self.search_user_role('reviewer')

    @property
    def roles(self):
        """Return all roles of this user"""
        roles = []
        for user_role in self.user_roles:
            roles.append(user_role.role)
        return roles

    @property
    def roles_available(self):
        roles = Role.query.filter(Role.active == True).all()
        available_roles = []
        for role in roles:
            if not self.has_role(role):
                available_roles.append(role)
        return available_roles

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

        if not cls.validate_username_and_email(username, email):
            raise UserAlreadyExist

        user = User()
        user.username = username
        user.email = email
        user.password = cls.generate_password(password)
        user.save()
        db.session.commit()
        return user

    @classmethod
    def validate_username_and_email(cls, username, email):
        email_user = cls.query.filter(User.username == username).first()
        name_user = cls.query.filter(User.email == email).first()
        if name_user or email_user:
            return False
        return True

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

    def search_user_role(self, role_name):
        try:
            role = Role.search_role(name=role_name, exactly=True)
            if self.has_role(role):
                return True
            return False
        except:
            return False

    def set_role(self, role):
        if self.has_role(role):
            raise UserAlreadyInRole

        user_role = UserRole()
        user_role.user = self
        user_role.role = role
        user_role.save(commit=True)

    def remove_role(self, role):
        user_role = UserRole.query.filter(UserRole.user == self, UserRole.role == role).first()

        if not user_role:
            raise UserNotHasRole

        db.session.delete(user_role)
        db.session.commit()

    def reload_stats(self):
        self.last_login_at = self.current_login_at
        self.current_login_at = datetime.now()
        self.login_count = self.login_count + 1
        self.save(commit=True)


class UserRole(Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'user_role'

    created_at = db.Column(db.DateTime, index=True, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship("User", backref="user_roles")
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id))
    role = db.relationship("Role", backref="role_users")

    __table_args__ = (db.UniqueConstraint('user_id', 'role_id', name='un_user_role'),)