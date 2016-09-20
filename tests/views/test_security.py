# coding: utf8
import pytest
from flask import url_for


@pytest.fixture()
def user_login(login, user):
    return login(username='Chewbaca', password='12345678')


def test_login_user_with_success(user_login):
    assert '<h3>Bem vindo Chewbaca da Silva!</h3>' in user_login.body.decode()


def test_login_user_without_success(login, user):
    response = login(username='Chewbaca', password='123456')
    assert 'Usuário ou senha inválido' in response.body.decode()


def test_logout(user_login, webtest):
    assert '<h3>Bem vindo Chewbaca da Silva!</h3>' in user_login.body.decode()
    response = webtest.get(url_for('security.logout')).maybe_follow()
    assert 'Usuário deslogado' in response.body.decode()
    response = webtest.get(url_for('security.dashboard')).maybe_follow()
    assert 'Faça o login antes de continuar' in response.body.decode()


def test_normal_user_in_access_restric_access(user_login, webtest):
    response = webtest.get(url_for('users.list_roles')).maybe_follow()
    assert '<h2>Você não tem permissão para acessar essa página</h2>' in response.body.decode()


def test_change_password_proccess_with_success(user_login, login, webtest):
    response = webtest.get(url_for('security.change_password')).maybe_follow()
    form = response.form
    form['old_password'] = '12345678'
    form['password'] = 'sw1234'
    form['confirm'] = 'sw1234'
    form.submit().maybe_follow()
    webtest.get(url_for('security.logout')).maybe_follow()
    response = login(username='Chewbaca', password='sw1234')
    assert '<h3>Bem vindo Chewbaca da Silva!</h3>' in response.body.decode()


@pytest.mark.parametrize('old_password, password, confirm, message',[
    ('1234567', 'sw1234', 'sw1234', 'Senha do usuário inválida!'),
    ('12345678', 'sw123', 'sw123', 'A senha tem de ter no mínimo 6 caracteres!'),
    ('12345678', 'sw1234', 'sw12345', 'Os campos senha e confirmação não estão iguais!')
])
def test_change_password_without_success(old_password, password, confirm, message, user_login, webtest):
    response = webtest.get(url_for('security.change_password')).maybe_follow()
    form = response.form
    form['old_password'] = old_password
    form['password'] = password
    form['confirm'] = confirm
    response = form.submit().maybe_follow()
    assert message == response.flashes[0][1]


def test_cached_session_send_to_dashboard(user_login, webtest):
    response = webtest.get(url_for('security.login')).maybe_follow()
    assert response.request.path == '/dashboard'
    assert response.template == 'security/dashboard.html'
