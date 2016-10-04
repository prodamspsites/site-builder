# coding: utf-8
import pytest
from flask import url_for

@pytest.mark.parametrize('view, kwargs, template', [
    ('core.list_projects', {},  'core/index.html'),
])
def test_templates(view, kwargs, template, su_login, webtest):
    response = webtest.get(url_for(view, **kwargs)).maybe_follow()
    assert response.template == template