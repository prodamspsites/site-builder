# coding: utf-8
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from builder.models import Model, db, User, Role
from builder.exceptions import UserAlreadyInRole, UserRoleNotFound


class UserRole(Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'user_role'

    created_at = db.Column(db.DateTime, index=True, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship("User", backref="user_roles")
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id))
    role = db.relationship("Role", backref="role_users")

    __table_args__ = (db.UniqueConstraint('user_id', 'role_id', name='un_user_role'),)

    @classmethod
    def set_role(cls, user, role):
        """Create a relationship of role and user"""
        try:
            user_role = cls()
            user_role.user_id = user.id
            user_role.role_id = role.id
            user_role.save()
            db.session.commit()
        except IntegrityError:
            raise UserAlreadyInRole

    @classmethod
    def delete_role(cls, user, role):
        user_role = cls.query.filter(cls.user == user, cls.role == role).first()
        if not user_role:
            raise UserRoleNotFound

        db.session.delete(user_role)
        db.session.commit()