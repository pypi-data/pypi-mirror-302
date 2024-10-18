from django.core.management.base import BaseCommand
from django.utils.timezone import now

from oauth_requests.models import Token


class Command(BaseCommand):
    help = "Removes expired OAuth 2.0 tokens."

    def handle(self, *args, **options):
        Token.objects.filter(expires_at__lte=now()).delete()
