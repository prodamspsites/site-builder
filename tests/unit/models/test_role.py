# coding: utf-8
import pytest
from builder.exceptions import RoleNotFound, RoleAlreadyExist, InvalidRoleName
from builder.models import Role


def test_create_role_with_success():
    created_role = Role.create(name='reviewer', description='Reviewer')
    role = Role.query.filter(Role.name == created_role.name).one()
    assert role.description == created_role.description


@pytest.mark.parametrize('exception, name', [
    (RoleAlreadyExist, 'admin'),
    (InvalidRoleName, '')
])
def test_should_not_create_role(admin_role, exception, name):
    with pytest.raises(exception):
        Role.create(name=name)


def test_edit_role_with_sucess(client_role):
    client_role.edit(name='user', description='Simple User')
    assert client_role.name == 'user'


@pytest.mark.parametrize('exception, name', [
    (RoleAlreadyExist, 'admin'),
    (InvalidRoleName, 'ad')
])
def test_should_not_edit_role(admin_role, exception, name):
    role = Role.create(name='user', description='Simple User')
    with pytest.raises(exception):
        role.edit(name=name)


def test_invalidate_and_validate_role(admin_role):
    admin_role.toggle_status()
    assert admin_role.is_active is False
    admin_role.toggle_status()
    assert admin_role.is_active is True


def test_search_role_with_name(admin_role):
    role = Role.search_role(name='admin', exactly=True)
    assert role.description == 'Administrador'


def test_search_role_with_part_of_name(admin_role):
    role_list = Role.search_role(name='ad', exactly=False)
    assert admin_role in role_list


def test_search_role_do_not_return_a_role():
    with pytest.raises(RoleNotFound):
        Role.search_role(name='Inexist role', exactly=True)