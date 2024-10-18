import requests
from requests.adapters import HTTPAdapter, Retry
from .logging import logger
from http import HTTPStatus


status_forcelist = (
    HTTPStatus.TOO_MANY_REQUESTS,
    HTTPStatus.BAD_GATEWAY,
    HTTPStatus.CONFLICT,
    HTTPStatus.LOCKED,
    HTTPStatus.SERVICE_UNAVAILABLE,
    HTTPStatus.GATEWAY_TIMEOUT,
    HTTPStatus.VARIANT_ALSO_NEGOTIATES,
    HTTPStatus.INSUFFICIENT_STORAGE,
    520,                                        # (Cloudflare) Web Server Returned an Unknown Error
    521,                                        # (Cloudflare) Web Server Is Down
    522,                                        # (Cloudflare) Connection Timed Out
    523,                                        # (Cloudflare) Origin Is Unreachable
    524,                                        # (Cloudflare) A Timeout Occurred
)


def setup(
        max_retries: int = 5,
        backoff_factor: float = 0.3,
        _status_forcelist: tuple[int] = status_forcelist
) -> requests.Session:

    logger.debug('setting up a new webhook session ..')
    session = requests.Session()
    retries = Retry(
        total=max_retries,
        read=max_retries,
        connect=max_retries,
        backoff_factor=backoff_factor,
        status_forcelist=_status_forcelist,
        raise_on_status=False,
        raise_on_redirect=False
    )

    adapter = HTTPAdapter(max_retries=retries)
    session.mount('https://', adapter)
    return session


def send(
        *urls: str,
        json: str | bool | list | dict = None,
        headers: dict[str, str] = None,
        max_retries: int = 5,
        backoff_factor: float = 0.3,
        _status_forcelist: tuple[int] = None,
        **kwargs
) -> list[requests.Response] | requests.Response | None:

    results = []
    for url in urls:

        # each url must have its own session to make sure
        # cross-requests parameters are not shared, like auth, cookies, etc ..
        s = setup(max_retries, backoff_factor, _status_forcelist)

        try:
            logger.info(f'sending webhook to {url} ..')
            res = s.post(url, json=json, headers=headers, **kwargs)
            results.append(res)
            logger.info(f'successfully sent webhook to {url}')

        except requests.exceptions.RequestException as e:
            logger.error(f'failed to send webhook to {url}\r\n{e}')
            return None

        logger.debug(f'closing webhook session ..')
        s.close()

    return results if len(results) > 1 else results[0]
