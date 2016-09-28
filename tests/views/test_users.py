# coding: utf-8
import pytest
from flask import url_for

from builder.models import User, Role, Invite


@pytest.fixture()
def admin_login(login, admin):
    return login(email='mayforce@bewith.me', password='12345678')


@pytest.mark.parametrize('view, kwargs, template', [
    ('users.list_users', {},  'users/list-users.html'),
    ('users.user_details', {'user_id': '1'}, 'users/details-user.html'),
    ('users.list_roles', {}, 'users/list-roles.html'),
    ('users.add_role', {}, 'users/add-role.html')
])
def test_templates(view, kwargs, template, su_login, webtest, user):
    response = webtest.get(url_for(view, **kwargs)).maybe_follow()
    assert response.template == template


@pytest.mark.parametrize('endpoint',[('users.user_details'),('users.toggle_user'),])
def test_set_unknown_id_in_user_details(endpoint, su_login, webtest):
    response = webtest.get(url_for(endpoint, user_id=9999))
    assert response.flashes == [('danger', 'Usuário não encontrado!')]
    response = response.maybe_follow()
    assert response.template == 'users/list-users.html'


def test_toggle_use_with_success(su_login, user, webtest):
    response = webtest.get(url_for('users.toggle_user', user_id=user.id))
    assert response.flashes == [('success', 'Usuário {} foi desativado.'.format(user.name))]
    user = User.query.get(user.id)
    assert user.active is False


def test_toggle_self_user_without_success(su_login, superuser, webtest):
    response = webtest.get(url_for('users.toggle_user', user_id=superuser.id))
    assert response.flashes == [('warning', 'Voce não pode alterar seus próprios usuário!')]


def test_add_role_with_success(su_login, webtest):
    response = webtest.get(url_for('users.add_role'))
    form = response.form
    form['name'] = 'test_role'
    form['description'] = 'Permissão de teste'
    form.submit().maybe_follow()
    role = Role.search_role(name='test_role', exactly=True)
    assert role.description == 'Permissão de teste'


@pytest.mark.parametrize('role_name, flashed_message', [
    ('superuser', [('danger', 'Permissão já existe!')]),
    ('', [('danger', 'Nome da permissão inválida!')])
])
def test_add_role_without_success(role_name, flashed_message, su_login, webtest):
    response = webtest.get(url_for('users.add_role'))
    form = response.form
    form['name'] = role_name
    response = form.submit()
    assert response.flashes == flashed_message


def test_toggle_role_with_success(su_login, admin_role, webtest):
    response = webtest.get(url_for('users.toggle_role', role_id=admin_role.id))
    assert response.flashes == [('success', 'Permissão {} foi desativado.'.format(admin_role.name))]
    role = Role.query.get(admin_role.id)
    assert role.active is False


def test_toggle_role_without_success(su_login, webtest):
    response = webtest.get(url_for('users.toggle_role', role_id=999))
    assert response.flashes == [('danger', 'Permissão não encontrada!')]
    response = response.maybe_follow()
    assert response.template == 'users/list-roles.html'


def test_set_role_to_user(su_login, user, admin_role, webtest):
    webtest.get(url_for('users.set_role', user_id=user.id, role_id=admin_role.id))
    user = User.query.get(user.id)
    assert user.roles[0].name == 'admin'


def test_set_superuser_without_success(admin_login, user, superuser_role, webtest):
    response = webtest.get(url_for('users.set_role', user_id=user.id, role_id=superuser_role.id))
    assert response.flashes == [('danger', 'Permissão de superusuário só pode ser atribuída por outro superusuário')]
    assert superuser_role not in user.roles


def test_unset_role_to_user(su_login, admin, admin_role, webtest):
    webtest.get(url_for('users.unset_role', user_id=admin.id, role_id=admin_role.id))
    user = User.query.get(admin.id)
    user.refresh()
    assert user.roles == []


def test_unset_superuser_without_success(admin_login, superuser, superuser_role, webtest):
    response = webtest.get(url_for('users.unset_role', user_id=superuser.id, role_id=superuser_role.id))
    assert response.flashes == [('danger', 'Permissão de superusuário só pode ser removida por outro superusuário')]
    assert superuser_role in superuser.roles


def test_remove_self_access_should_be_failed(su_login, superuser, superuser_role, webtest):
    response = webtest.get(url_for('users.unset_role', user_id=superuser.id, role_id=superuser_role.id))
    assert response.flashes == [('info', 'Não pode remover seus próprios acessos!')]
    assert superuser_role in superuser.roles


def test_set_already_added_permission(su_login, superuser, superuser_role, webtest):
    response = webtest.get(url_for('users.set_role', user_id=superuser.id, role_id=superuser_role.id))
    assert response.flashes == [('info', 'Usuário já tem essa permissão!')]


def test_untset_already_removed_permission(su_login, admin, superuser_role, webtest):
    response = webtest.get(url_for('users.unset_role', user_id=admin.id, role_id=superuser_role.id))
    assert response.flashes == [('info', 'Usuário já não tem essa permissão!')]


def test_set_permission_to_inexistent_user(su_login, admin_role, webtest):
    response = webtest.get(url_for('users.set_role', user_id=999, role_id=admin_role.id))
    assert response.flashes == [('danger', 'Erro ao adicionar permissão!')]


def test_unset_permission_to_inexistent_user(su_login, admin_role, webtest):
    response = webtest.get(url_for('users.unset_role', user_id=999, role_id=admin_role.id))
    assert response.flashes == [('danger', 'Erro ao remover permissão!')]


def test_set_inexistent_permission(su_login, admin, webtest):
    response = webtest.get(url_for('users.set_role', user_id=admin.id, role_id=999))
    assert response.flashes == [('danger', 'Erro ao adicionar permissão!')]


def test_unset_inexistent_permission(su_login, admin, webtest):
    response = webtest.get(url_for('users.unset_role', user_id=admin.id, role_id=999))
    assert response.flashes == [('danger', 'Erro ao remover permissão!')]


def test_invite_user_with_success(su_login, webtest):
    response = webtest.get(url_for('users.invites'))
    form = response.form
    form['name'] = 'User de Teste'
    form['email'] = 'teste@invite.com'
    form.submit().maybe_follow()
    invite = Invite.get_invite('teste@invite.com')
    assert invite.guest.name == 'User de Teste'


@pytest.mark.parametrize('name, email, message', [
    ('Darth Vader', '', [('danger', 'O email é inválido!')]),
    ('', 'darth_vader@sw.com', [('danger', 'O campo nome está vazio!')]),
    ('Darth Vader', 'mayforce@bewith.you', [('warning', 'O email mayforce@bewith.you já foi utilizado!')])
])
def test_invite_user_without_sucess(name, email, message, su_login, webtest):
    response = webtest.get(url_for('users.invites'))
    form = response.form
    form['name'] = name
    form['email'] = email
    response = form.submit()
    assert response.flashes == message
    assert Invite.query.count() == 0