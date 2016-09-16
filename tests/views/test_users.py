# coding: utf-8
import pytest
from flask import url_for


@pytest.mark.parametrize('view, kwargs, template', [
    ('users.list_users', {},  'users/list-users.html'),
    ('users.add_user', {}, 'users/add-user.html'),
    ('users.user_details', {'user_id': '1'}, 'users/details-user.html'),
    ('users.list_roles', {}, 'users/list-roles.html'),
    ('users.add_role', {}, 'users/add-role.html')
])
def test_all_user_templates_with_success(view, kwargs, template, su_login, webtest, user):
    response = webtest.get(url_for(view, **kwargs)).maybe_follow()
    assert response.template == template


def test_set_unknown_id_in_user_details(su_login, webtest):
    response = webtest.get(url_for('users.user_details', user_id=9999))
    assert response.flashes == [('info', 'Usuário não existe!')]
    response = response.maybe_follow()
    assert response.template == 'users/list-users.html'