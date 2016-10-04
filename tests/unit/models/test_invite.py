# coding: utf-8
import pytest

from builder.models import Invite
from builder.exceptions import UserNotFound, InviteNotFound, InvalidToken


def test_invite_user_with_success_and_get_invite(superuser):
    guest = {'guest_name': 'test complete', 'guest_email': 'test-complete@invite.com'}
    Invite.create_invite(host=superuser, **guest)
    invite = Invite.get_invite(guest_email=guest['guest_email'])
    assert invite.guest.name == guest['guest_name']
    assert invite.host.name == 'Anakin Skywalker'


@pytest.mark.parametrize('email, exception', [
    ('inexistent@invite.com', UserNotFound),
    ('mayforce@bewith.you', InviteNotFound)])
def test_get_invite_exceptions_errorrs(email, exception, superuser):
    with pytest.raises(exception):
        Invite.get_invite(email)


def test_validate_invite(invite):
    assert invite.is_valid() == True


def test_accept_invite_should_update_status_and_invalidate(invite):
    invite.accept(temporary_token=invite.guest.temporary_token, password='123456', confirm_password='123456')
    assert invite.current_status == 'aceito'
    assert invite.is_valid() == False


def test_accept_should_raise_invalid_token(invite):
    invite.accept(temporary_token=invite.guest.temporary_token, password='123456', confirm_password='123456')
    with pytest.raises(InvalidToken):
        invite.accept(temporary_token='12345', password='123456', confirm_password='123456')


def test_view_invite_should_update_status(invite):
    invite.view()
    assert invite.current_status == 'visualizado'
    assert invite.is_valid() == True


def test_invalidate_invite(expired_invite):
    expired_invite.view()
    assert expired_invite.current_status == 'inválido'
    assert expired_invite.is_valid() == False


def test_sent_email_without_change_expire_date(superuser):
    guest = {'guest_name': 'test complete', 'guest_email': 'test-complete@invite.com'}
    invite = Invite.create_invite(host=superuser, **guest)
    invite.send()

    assert invite.sent_count == 1
    assert invite.current_status == 'enviado'

    invite.refresh()
    invite.send()

    assert invite.sent_count == 2
    assert invite.current_status == 'reenviado'


def test_sent_email_with_change_expire_date(expired_invite):
    original_expired_date = expired_invite.expire_at
    expired_invite.send()
    assert expired_invite.expire_at > original_expired_date
