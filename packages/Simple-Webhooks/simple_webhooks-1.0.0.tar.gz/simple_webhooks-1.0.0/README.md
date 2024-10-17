# Webhooks

This *lightweight* Python package provides flexible way to send webhooks to one or more URLs, with retry mechanisms and support for various webhook configurations.

## Features
- Send webhook to multiple URLs.
- Retry failed webhook requests.
- Extensible to support custom webhook logic.

## Installation

```bash
pip install webhooks
```

## usage


```python
from webhooks import RetryWebhookSender, WebhookManager


sender = RetryWebhookSender()
manager = WebhookManager(sender)
res = manager.send_to_multiple(
    ['https://www.example.com/webhook'],
    {'event': 'my_event'}
)

for result in res:
    print(result.status_code)

```
