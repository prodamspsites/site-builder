# coding: utf-8
import re
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from builder.exceptions import InvalidRoleName, RoleAlreadyExist, RoleNotFound
from builder.models import Model, db


class Role(Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'role'

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.now())

    @property
    def is_active(self):
        """Return current status of role"""
        return self.active

    @classmethod
    def create(cls, name, description=None):
        """Create new role"""
        if not cls.verify_role_name(name):
            raise InvalidRoleName

        try:
            role = Role()
            role.name = name
            role.description = description
            role.save()
            db.session.commit()
            return role
        except IntegrityError:
            raise RoleAlreadyExist

    def edit(self, name=None, description=None):
        """Edit existent role"""
        try:
            if name:
                if not self.verify_role_name(name):
                    raise InvalidRoleName
                self.name = name
            if description:
                self.description = description
            self.save()
            db.session.commit()
        except IntegrityError:
            raise RoleAlreadyExist
        return self

    @classmethod
    def search_role(cls, name, exactly=False):
        """Search role by name, exactly or not"""
        if exactly:
            role = cls.query.filter(Role.name == name).first()
        else:
            role = cls.query.filter(Role.name.contains(name)).all()
        if not role:
            raise RoleNotFound
        return role

    @staticmethod
    def verify_role_name(role_name):
        """Check length and if the username does not contains invalid chars"""
        if len(role_name) >= 3 and re.search(r'^[a-zA-Z0-9_.-]+$', role_name):
            return True

    @property
    def users(self):
        """Return all users in this role"""
        users = []
        for role_user in self.role_users:
            users.append(role_user.user)
        return users

    def remove_all_users(self):
        """Remove all users in this role"""
        for role_user in self.role_users:
            role_user.delete(commit=True)
        db.session.commit()