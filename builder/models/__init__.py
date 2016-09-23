# coding: utf-8
from flask_sqlalchemy import BaseQuery
from sqlalchemy import func

from builder.exceptions import SessionNotFound
from builder.main import db


class ModelMixin(object):
    _new = False

    patchable = ()
    unpatchable = ()

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.flush()

    def refresh(self):
        if not self._sa_instance_state.session:
            raise SessionNotFound("You can't refresh an object that has no session.")

        self._sa_instance_state.session.refresh(self)

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()

    def toggle_status(self):
        if self.active:
            self.active = False
        else:
            self.active = True
        self.save()
        db.session.commit()

    def __repr__(self):
        field = value = None
        for f in ('name', 'username', 'created', 'uuid'):
            if hasattr(self, f):
                field = f
                value = getattr(self, f)
                break
        if field:
            return "<{name}[{id!r}] {field}={value!r}>".format(
                name=self.__class__.__name__, id=self.id, field=field, value=value)
        else:
            return "<{name}[{id!r}]>".format(
                name=self.__class__.__name__, id=self.id)


class Query(BaseQuery):
    def fast_count(self):
        """For complicated reasons, SQLAlchemy doesn't do a `count(*)` when
        you call `query.count()`. Instead, it retrieves the whole resultset in a
        subquery and runs the `count('*')` on it, which is terribly slow
        sometimes.
        This method converts the select clause of the query to a single
        `func.count('*')` statement, allowing for much faster count.
        """

        counter = self.with_entities(func.count('*'))

        if counter.whereclause is None:
            counter = counter.select_from(self._entities[0].type)

        return counter.scalar()


class Model(db.Model, ModelMixin):
    __abstract__ = True
    query_class = Query


from builder.models.user import User, UserRole # noqa
from builder.models.role import Role # noqa
from builder.models.invite import Invite # noqa
