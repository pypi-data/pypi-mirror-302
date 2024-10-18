# [django-oauth-requests](https://pypi.org/project/django-oauth-requests/)
OAuth 2.0 authentication with [Django](https://www.djangoproject.com/) and [requests](https://requests.readthedocs.io/) made simple.

This app is for authenticating with remote APIs that use OAuth 2.0. It saves issued tokens to a database and automatically takes care of refreshing them after their expiration.

# Installation
Use a package manager to install it, for example using this command in your terminal:
```
pip install django-oauth-requests
```

# Setup
First, add `oauth_requests` into your `INSTALLED_APPS` in the `settings.py` file:
```python
INSTALLED_APPS = [
    …
    "oauth_requests",
]
```

Then, add a configuration for all the services you plan to use, like this sample:

```python
OAUTH_REQUESTS = {
    "paypal": {
        "client_id": "your-paypal-client_id",
        "client_secret": "your-paypal-client_secret",
        "url": "https://api-m.sandbox.paypal.com/v1/oauth2/token",
    },
}
```

In this example, we only defined one service called `paypal`. We should put there issued `CLIENT_ID` and `CLIENT_SECRET` strings under their respective keys. And `url` should point to the authentication endpoint for issuing tokens.

And finally, we should run Django migration to create tables for storing issued tokens. We can accomplish this by running the following command in our terminal:

```
python manage.py migrate oauth_requests
```

# Usage
In the actual code, use the `OAuth` class to issue OAuth 2.0 token for your service and start to use it with `requests`:

```python
import requests
from oauth_requests import OAuth

oauth = OAuth("paypal")

# start sending requests using the issued token
response = requests.get("https://api-m.sandbox.paypal.com/v2/invoicing/invoices", auth=oauth)

# optionally, you can use requests.Session
session = requests.Session()
session.auth = oauth

response = session.get("https://api-m.sandbox.paypal.com/v2/invoicing/invoices")
```
