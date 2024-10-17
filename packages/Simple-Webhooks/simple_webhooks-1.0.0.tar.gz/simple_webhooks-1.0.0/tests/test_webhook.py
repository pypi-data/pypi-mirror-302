from http import HTTPStatus
import pytest
from unittest.mock import Mock, patch
from webhook import RetryWebhookSender
from requests.exceptions import ConnectionError, SSLError, RequestException


@patch('requests.Session.post')
def test_send_successful(req):
    res = Mock()
    res.status_code = HTTPStatus.OK
    req.return_value = res

    sender = RetryWebhookSender()
    url = "https://example.com/webhook"
    payload = {"event": "test_event"}
    sender.send(url, payload)

    assert req.call_count == 1
    assert res.status_code == HTTPStatus.OK


@patch('requests.Session.post')
def test_send_http_faliure(req):
    res = Mock()
    res.status_code = HTTPStatus.SERVICE_UNAVAILABLE
    req.return_value = res

    sender = RetryWebhookSender()
    url = "https://example.com/webhook"
    payload = {"event": "test_event"}
    sender.send(url, payload)

    assert req.call_count == 1
    assert res.status_code == HTTPStatus.SERVICE_UNAVAILABLE


@patch('requests.Session.post')
def test_send_connection_faliure(req):
    req.side_effect = [ConnectionError(), SSLError()]

    sender = RetryWebhookSender()
    url = "https://example.com/webhook"
    payload = {"event": "test_event"}

    with pytest.raises(RequestException):
        sender.send(url, payload)
