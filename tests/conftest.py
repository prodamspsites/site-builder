# coding: utf-8
import os

os.environ['AUTH_ENV'] = 'test'
os.environ['SECRET_KEY'] = 'test'

import pytest
from flask.testing import FlaskClient
from builder.main import db



def monkey_patch_sqlalchemy():
    """
    Replaces the SQLAlchemy `session.remove` method with a NOP. This avoids
    that any uncommited data is removed from session during the teardown hooks.
    You want to keep the data on session during the tests otherwise you won't
    be able to run any assertion on the database.
    Also replaces the `session.commit` with the `session.flush`. This is done
    for performance reasons and to avoid recreating the database on every test.
    """
    from sqlalchemy.orm import scoped_session
    scoped_session.original_remove = scoped_session.remove
    scoped_session.remove = lambda self: None

    scoped_session.original_commit = scoped_session.commit
    scoped_session.commit = scoped_session.flush


def pytest_configure():
    monkey_patch_sqlalchemy()


def pytest_runtest_call(item):
    """
    If the ``flush`` fixture is included, execute a db flush just before the
    test starts.
    """
    if 'flush' in item.fixturenames:
        db.session.flush()


@pytest.fixture(scope='session')
def session_app():
    """
    Creates a new Flask application for a test duration.
    Uses application factory `create_app`.
    """
    from builder.main import create_app
    _app = create_app()
    _app.test_client_class = FlaskClient

    return _app


@pytest.yield_fixture()
def app(session_app):
    ctx = session_app.test_request_context()
    ctx.push()
    yield session_app
    ctx.pop()


@pytest.yield_fixture
def request_context(app):
    """
    Some tests require a request context and do not care about which endpoint is being used. E.g.: Using
    ``flask.url_for`` usually requires a request context.
    """
    ctx = app.test_request_context('/')
    ctx.push()
    yield ctx
    ctx.pop()


@pytest.fixture(scope='session')
def database(session_app):
    ctx = session_app.test_request_context()
    ctx.push()
    db.create_all()
    ctx.pop()


@pytest.yield_fixture()
def db_session(database, app):
    db.session.original_remove()
    db.session.begin(subtransactions=True)
    yield db.session
    db.session.rollback()


@pytest.fixture(autouse=True)
def all(request, app, db_session):
    if request.cls:
        request.cls.app = app
    # This fix is to use the `all()` built-in function normally
    return __builtins__['all']