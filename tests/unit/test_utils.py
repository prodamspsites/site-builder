# coding: utf-8
import mock
from datetime import datetime

from builder.utils import convert_time, send_email


def test_time_should_return_in_current_format():
    random_datetime = datetime(day=10, month=12, year=2018, hour=00, minute=23, second=3)
    assert convert_time(random_datetime) == '10/12/2018 00:23'


def test_time_should_return_a_custom_format():
    random_datetime = datetime(day=10, month=12, year=2018, hour=00, minute=23, second=3)
    format = '%Y/%m/%d %H:%M'
    assert convert_time(random_datetime, format) == '2018/12/10 00:23'


def test_string_should_return_error():
    random_datetime_string = '2018/12/10 00:23'
    assert convert_time(random_datetime_string) == '-'


@mock.patch('flask_mail.Mail.send')
def test_email_sender_call_function(send_mock):
    email_kwargs = {
        'sender': 'no-reply@test',
        'recipient': 'test@test',
        'subject': 'Test simple email',
        'html': '<b>Test</b>',
    }
    send_email(**email_kwargs)
    assert send_mock.call_count == 1
