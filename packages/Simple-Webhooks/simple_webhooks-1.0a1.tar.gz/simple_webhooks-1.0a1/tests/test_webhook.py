from http import HTTPStatus
import pytest
from unittest.mock import Mock, patch
import webhooks
from requests.exceptions import RequestException


@patch('requests.Session.post')
def test_send_successful(req):
    res = Mock()
    webhooks.send(
        "https://example.com/webhook",
        json={"event": "test_event"}
    )

    res.status_code = HTTPStatus.OK
    req.return_value = res

    assert req.call_count == 1
    assert res.status_code == HTTPStatus.OK


@patch('requests.Session.post')
def test_send_successful_multiple(req):
    res = Mock()
    webhooks.send(
        "https://example.com/webhook", "https://domain.com/webhook",
        json={"event": "test_event"}
    )

    res.status_code = HTTPStatus.OK
    req.return_value = res

    assert req.call_count == 2
    assert res.status_code == HTTPStatus.OK


@patch('requests.Session.post')
def test_send_unsuccessful(req):
    res = Mock()
    webhooks.send(
        "https://example.com/webhook",
        json={"event": "test_event"}
    )

    res.status_code = HTTPStatus.BAD_GATEWAY
    req.return_value = res

    assert req.call_count == 1
    assert res.status_code == HTTPStatus.BAD_GATEWAY


@patch('requests.Session.post')
def test_send_unsuccessful_multiple(req):
    res = Mock()
    webhooks.send(
        "https://example.com/webhook", "https://domain.com/webhook",
        json={"event": "test_event"}
    )

    res.status_code = HTTPStatus.BAD_GATEWAY
    req.return_value = res

    assert req.call_count == 2
    assert res.status_code == HTTPStatus.BAD_GATEWAY


@patch('requests.Session.post')
def test_send_exception(req):
    req.side_effect = RequestException()
    res = webhooks.send(
        "https://example.com/webhook",
        json={"event": "test_event"}
    )
    assert req.call_count == 1
    assert res is None


@patch('requests.Session.post')
def test_send_exception_multiple(req):
    req.side_effect = RequestException()
    res = webhooks.send(
        "https://example.com/webhook", "https://domain.com/webhook",
        json={"event": "test_event"}
    )
    assert req.call_count == 1
    assert res is None
