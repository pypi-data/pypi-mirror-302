from django.conf import settings
from django.db import models

Service = models.TextChoices(
    "Service",
    {service.upper(): service for service in getattr(settings, "OAUTH_REQUESTS", {})},
)


class Token(models.Model):
    service = models.CharField(max_length=16, choices=Service)
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=["service", "created_at"]),
        ]

    def __str__(self) -> str:
        return self.token
