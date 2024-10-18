from datetime import timedelta

import requests
from django.conf import settings
from django.utils.timezone import now

OAUTH_REQUESTS = getattr(settings, "OAUTH_REQUESTS", {})


class OAuthError(Exception):
    pass


class OAuth:
    def __init__(self, service) -> None:
        if service not in OAUTH_REQUESTS:
            raise OAuthError(f"Service {service} not found in OAUTH_REQUESTS. Please set it up.")

        conf = OAUTH_REQUESTS[service]

        if not isinstance(conf, dict):
            raise OAuthError(f'OAUTH_REQUESTS["{service}"] needs to be a dictionary.')

        for field in ("client_id", "client_secret", "url"):
            if not conf.get(field):
                raise OAuthError(f"Configuration {field} is missing for {service}. Please add it to OAUTH_REQUESTS.")

        self.service = service

        from .models import Token

        self.token = Token.objects.filter(service=service, expires_at__gt=now()).first()

        if not self.token:
            response = requests.post(
                conf["url"],
                {"grant_type": "client_credentials"},
                headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
                auth=(conf["client_id"], conf["client_secret"]),
            )

            if response.ok:
                data = response.json()
                self.token = Token.objects.create(
                    service=service,
                    token=data.get("access_token") or "",
                    expires_at=now() + timedelta(seconds=data.get("expires_at") or 0),
                )
            else:
                response.raise_for_status()

    def __call__(self, request):
        request.headers["Authorization"] = f"Bearer {self.token.token}"
        return request
