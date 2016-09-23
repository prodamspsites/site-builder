# coding: utf-8
import re
import random
import string
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from builder.exceptions import (InvalidPassword, InvalidUsername, InvalidEmail, PasswordMismatch, UserAlreadyExist,
                                UserNotFound, UserNotHasRole, InvalidCredentials, UserAlreadyInRole, EmptyUserName)
from builder.models import Model, db
from builder.models.role import Role


class User(Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'user'

    # Required Informations
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # Statuses
    active = db.Column(db.Boolean(), default=True)
    confirmed = db.Column(db.Boolean(), default=False)

    # Statistics
    created_at = db.Column(db.DateTime, index=True, default=datetime.now())
    last_login_at = db.Column(db.DateTime())
    confirmed_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    login_count = db.Column(db.Integer(), default=0)

    # Others info
    temporary_token = db.Column(db.String(20))

    @property
    def superuser(self):
        """Return superuser status"""
        return self.search_user_role('superuser')

    @property
    def admin(self):
        """Return admin status"""
        return self.search_user_role('admin')

    @property
    def client(self):
        """Return client status"""
        return self.search_user_role('client')

    @property
    def roles(self):
        """Return all roles of this user"""
        roles = []
        for user_role in self.user_roles:
            roles.append(user_role.role)
        return roles

    @property
    def roles_available(self):
        """Return roles available to attached in this user"""
        roles = Role.query.filter(Role.active == True).all()
        available_roles = []
        for role in roles:
            if not self.has_role(role):
                available_roles.append(role)
        return available_roles

    @classmethod
    def by_email(cls, email):
        """Search user by email"""
        user = cls.query.filter(User.email == email).first()
        if not user:
            raise UserNotFound
        return user

    @classmethod
    def create(cls, email, name, password, confirm_password):
        """ Create a new user """
        if not cls.verify_email(email):
            raise InvalidEmail

        if len(password) < 6:
            raise InvalidPassword

        if password != confirm_password:
            raise PasswordMismatch

        if cls.validate_existent_email(email):
            raise UserAlreadyExist

        if not name:
            raise EmptyUserName

        user = User()
        user.email = email
        user.name = name
        user.password = cls.generate_password(password)
        user.save()
        db.session.commit()
        return user

    @classmethod
    def validate_existent_email(cls, email):
        """Validate if username and email are available"""
        user = cls.query.filter_by(email=email).first()
        if user:
            return True
        return False

    @classmethod
    def generate_password(cls, password=None):
        """Create hash when password set or create a random password"""
        if not password:
            password = cls.random_password(12)
        return generate_password_hash(password)

    @staticmethod
    def random_password(size=12):
        """Create a string for password"""
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

    @staticmethod
    def verify_email(email):
        """Check if the email contains valid format"""
        if re.search(r'[\w.-]+@[\w.-]+.\w+', email):
            return True

    def change_password(self, old_password, password, confirm_password):
        """Change password of user"""
        if len(password) < 6:
            raise InvalidPassword

        if password != confirm_password:
            raise PasswordMismatch

        self.validate_password(old_password)
        self.password = self.generate_password(password)
        self.save()
        db.session.commit()

    def validate_password(self, password):
        """Used for validate hash password"""
        if check_password_hash(self.password, password):
            return True
        else:
            raise InvalidCredentials

    def has_role(self, role):
        """Verify if this user have role"""
        if role in self.roles:
            return True

    def search_user_role(self, role_name):
        try:
            role = Role.search_role(name=role_name, exactly=True)
            if self.has_role(role):
                return True
            return False
        except:
            return False

    def set_role(self, role):
        """Set role to self user"""
        if self.has_role(role):
            raise UserAlreadyInRole

        user_role = UserRole()
        user_role.user = self
        user_role.role = role
        user_role.save(commit=True)

    def remove_role(self, role):
        """Remove role to self user"""
        user_role = UserRole.query.filter(UserRole.user == self, UserRole.role == role).first()

        if not user_role:
            raise UserNotHasRole

        db.session.delete(user_role)
        db.session.commit()

    def reload_stats(self):
        """Reload all stats for login"""
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