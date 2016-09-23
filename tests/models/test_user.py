# coding: utf-8
import pytest
import mock

from builder.exceptions import (UserAlreadyExist, InvalidUsername, InvalidEmail, InvalidPassword, PasswordMismatch,
                                UserNotFound, InvalidCredentials, UserAlreadyInRole, UserNotHasRole, EmptyUserName)
from builder.models import User


def test_create_user_with_success():
    User.create(email='test1@gmail.com',
                name='test',
                password='12345678',
                confirm_password='12345678')
    user = User.query.filter_by(email='test1@gmail.com').one()
    assert user.name == 'test'


@pytest.mark.parametrize('exception, name, email, password, confirm_password', [
    (UserAlreadyExist, 'Chewbaca da Silva', 'chewe@solo.com', '12345678', '12345678'),
    (InvalidEmail, 'teste', 'itsnotvalidemail', '12345678', '12345678'),
    (InvalidPassword, 'teste', 'test1@gmail.com', '', ''),
    (PasswordMismatch, 'teste', 'test1@gmail.com', '12345678', '87654321'),
    (EmptyUserName, '', 'test1@gmail.com', '12345678', '12345678')
])
def test_create_user_raises_error(user, exception, name, email, password, confirm_password):
    with pytest.raises(exception):
        User.create(email=email, name=name, password=password, confirm_password=confirm_password)


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


def test_get_user_with_email(user):
    user = User.by_email('chewe@solo.com')
    assert str(user) == '<User[1] name=\'Chewbaca da Silva\'>'


def test_get_inexistent_user():
    with pytest.raises(UserNotFound):
        User.by_email('luke@skywalker.com')


def test_return_true_in_valid_password(user):
    assert user.validate_password('12345678') is True


# def test_return_none_in_invalid_password(user):
#     assert user.validate_password('None') is None


def test_invalidate_and_validate_user(user):
    user.toggle_status()
    assert user.active is False
    user.toggle_status()
    assert user.active is True


def test_if_is_a_superuser(superuser, user):
    assert superuser.superuser is True
    assert user.superuser is False


def test_set_role_to_user(user, admin_role):
    user.set_role(admin_role)
    assert user.has_role(admin_role) is True


def test_should_raise_error_in_duplicate_user_role(superuser, superuser_role):
    with pytest.raises(UserAlreadyInRole):
        superuser.set_role(superuser_role)


def test_should_raise_error_in_remove_wrong_role(superuser, admin_role):
    with pytest.raises(UserNotHasRole):
        superuser.remove_role(admin_role)


def test_available_roles(superuser, admin_role, client_role):
    assert superuser.roles_available == [admin_role, client_role]
    superuser.set_role(client_role)
    assert superuser.client == True
    assert superuser.roles_available == [admin_role]