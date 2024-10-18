# django-client-ip

`django-client-ip` is a Django middleware that retrieves the client IP address and optionally fetches geolocation data using `ip-api.com`.

## Installation

1. Install the package using pip:
```bash
pip install django-client-ip
```

2. Add the middleware to your Django project in settings.py:
```python
MIDDLEWARE = [
    # Other middlewares
    'django_client_ip.GetClientIP',
]
```

## Usage
Once installed, every `request` object will have a `client_ip` attribute containing the IP address and geolocation data (if available).

## Author
[Hadi Cahyadi](mailto:cumulus13@gmail.com)

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cumulus13)

[![Donate via Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cumulus13)
 [Support me on Patreon](https://www.patreon.com/cumulus13)

