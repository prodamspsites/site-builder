# coding: utf-8
import pytest
import mock

from builder.exceptions import (UserAlreadyExist, InvalidUsername, InvalidEmail, InvalidPassword, PasswordMismatch,
                             UserNotFound, InvalidCredentials)
from builder.models import User


def test_create_user_with_success():
    User.create(username='testuser', email='test1@gmail.com', password='12345678', confirm_password='12345678')
    user = User.query.filter_by(username='testuser').one()
    assert user.email == 'test1@gmail.com'


@pytest.mark.parametrize('exception, username, email, password, confirm_password', [
    (UserAlreadyExist, 'Chewbaca', 'chew@solo.com', '12345678', '12345678'),
    (InvalidUsername, '', 'test1@gmail.com', '12345678', '12345678'),
    (InvalidUsername, 'test@user', 'test1@gmail.com', '12345678', '12345678'),
    (InvalidEmail, 'testuser', 'itsnotvalidemail', '12345678', '12345678'),
    (InvalidPassword, 'testuser', 'test1@gmail.com', '', ''),
    (PasswordMismatch, 'testuser', 'test1@gmail.com', '12345678', '87654321'),
])
def test_create_user_raises_error(user, exception, username, email, password, confirm_password):
    with pytest.raises(exception):
        User.create(username=username, email=email, password=password, confirm_password=confirm_password)


def test_change_user_password_with_success(user):
    user.change_password(old_password='12345678', password='87654321', confirm_password='87654321')
    valid = user.validate_password('87654321')
    assert valid is True


@pytest.mark.parametrize('exception, old_password, password, confirm_password', [
    (InvalidCredentials, 'password_error', '12345678', '12345678'),
    (InvalidPassword, '12345678', '', ''),
    (PasswordMismatch, '12345678', '1234567890', '0987654321'),
])
def test_change_password_errors(user, exception, old_password, password, confirm_password):
    with pytest.raises(exception):
        user.change_password(old_password=old_password, password=password, confirm_password=confirm_password)


def test_get_user_with_username(user):
    user = User.by_login('Chewbaca')
    assert user.email == 'chewe@solo.com'


def test_get_user_with_email(user):
    user = User.by_login('chewe@solo.com')
    assert str(user) == '<User[1] username=\'Chewbaca\'>'


def test_get_inexistent_user():
    with pytest.raises(UserNotFound):
        User.by_login('Luke_Skywalker')


def test_return_true_in_valid_password(user):
    assert user.validate_password('12345678') is True


def test_return_none_in_invalid_password(user):
    assert user.validate_password('None') is None


def test_invalidate_and_validate_user(user):
    user.toggle_status()
    assert user.active is False
    user.toggle_status()
    assert user.active is True


def test_if_is_a_superuser(superuser, user):
    assert superuser.superuser is True
    assert user.superuser is False

