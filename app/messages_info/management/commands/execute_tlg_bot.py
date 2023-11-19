import logging
from django.core.management.base import BaseCommand

from app.connectors import TelegramExecuteConnector

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)


class Command(BaseCommand):
    help = 'Execute Telegram Bot'

    def handle(self, *args, **options):

        tlg = TelegramExecuteConnector()
        tlg()
