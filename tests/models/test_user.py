# coding: utf-8
def test_if_is_a_superuser(superuser, user):
    assert superuser.is_superuser is True
    assert user.is_superuser is False