from abc import ABC, abstractmethod
import requests
from requests.adapters import HTTPAdapter, Retry
from .logging import logger
from http import HTTPStatus


class WebhookSender(ABC):
    """
    Abstract base class for sending webhooks.
    Ensures adherence to Open/Closed and Dependency Inversion principles by
    allowing webhook senders to use different implementations of the send method.
    """

    @abstractmethod
    def send(self, url: str, payload: dict) -> requests.Response:
        """
        Abstract method to send a webhook to a given URL with the provided payload.
        Subclasses must implement this method.
        """
        pass

    @abstractmethod
    def setup(self) -> None:
        """
        Abstract method to setup the sender including retries and session
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """
        Abstract method to reset webhook sender session.
        """
        pass


class RetryWebhookSender(WebhookSender):
    """
    Concrete implementation of WebhookSender that sends a simple webhook via HTTP POST.
    Adheres to the Single Responsibility Principle.
    """

    def __init__(
            self,
            retries: int = 5,
            backoff_factor: float = 0.2,
            statuses: tuple[int] = (
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
    ) -> None:

        WebhookSender.__init__(self)
        self.session = None
        self.retries = None
        self.retries_count = retries
        self.backoff_factor = backoff_factor
        self.statuses = statuses
        self.setup()
        logger.debug(f'{self.__name__} initialized and set up.')

    def setup(self):
        self.session = requests.Session()
        self.retries = Retry(
            total=self.retries_count,
            read=self.retries_count,
            connect=self.retries_count,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.statuses,
            raise_on_status=False,
            raise_on_redirect=False
        )
        adapter = HTTPAdapter(max_retries=self.retries)
        self.session.mount('https://', adapter)

    def reset(self):
        self.setup()
        logger.debug(f'{self.__name__} was resetted.')

    def send(self, url: str, payload: dict = None) -> requests.Response:
        logger.info(f'{self.__name__} sending webhook to {url} ..')
        res = self.session.post(url, json=payload)
        logger.info(f'{self.__name__} successfully sent webhook to {url}')
        return res
