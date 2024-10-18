# Webhooks

This *lightweight* Python package provides flexible way to send webhooks to one or more URLs, with retry mechanisms and support for various webhook configurations.

## Features
- Send webhook to multiple URLs.
- Automatically retry failed webhook requests.
- Secure and reliable way to handle webhooks
- Simple and straight forward
- Extensible by design
- Currently, supports json payload only

## Installation

```bash
pip install simple-webhooks
```

## Usage

```python
import webhooks


res = webhooks.send(
    'https://www.example.com/webhook', 'https://www.domain.com/webhook',
    json={'event': 'my_event'}
)
for result in res:
    print(result.status_code)
```
