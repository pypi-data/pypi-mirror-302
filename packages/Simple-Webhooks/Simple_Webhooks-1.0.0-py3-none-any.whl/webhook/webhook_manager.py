from .webhook_sender import WebhookSender
from requests import Response


class WebhookManager:
    """
    Manages sending webhooks to multiple URLs.
    Adheres to Single Responsibility and Open/Closed principles by delegating
    the sending functionality to different WebhookSender implementations.
    """

    def __init__(self, sender: WebhookSender):
        """
        Initializes with a WebhookSender implementation.
        Follows Dependency Inversion by depending on an abstraction (WebhookSender).
        """
        self.sender = sender

    def send_to_multiple(self, urls: list[str], payload: dict) -> list[Response]:
        """
        Sends the payload to multiple URLs using the provided sender.
        """

        res = []
        for url in urls:
            result = self.sender.send(url, payload)
            res.append(result)
            self.sender.reset()

        return res
