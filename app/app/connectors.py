
from django.core import management
from typing import Any
from telegram import Bot, Update
import asyncio
from typing import Callable
from app.settings import TELEGRAM_TOKEN
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Application


class TelegramSendMessageConnector:

    def __init__(
        self,
        token: str,
        chat_id: int,
        message: str
    ) -> None:
        self.token = token
        self.chat_id = chat_id
        self.message = message
        self.bot = Bot(token=self.token)

    def __call__(self, *args: Any, **kwds: Any) -> None:
        self.loop_report(self.send_report_to_telegram())

    async def send_report_to_telegram(self) -> Callable[[None], None]:
        await self.bot.send_message(chat_id=self.chat_id, text=self.message)

    def loop_report(self, operation: Callable[..., None]) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            operation)


class TelegramExecuteConnector:

    def __init__(
        self,
        chat_id: int = 401089055
    ) -> None:
        self.token = TELEGRAM_TOKEN
        self.application = ApplicationBuilder().token(
            self.token).post_init(self.post_init).post_stop(self.post_stop).build()
        self.chat_id = chat_id

    def __call__(self,
                 *args: Any,
                 **kwds: Any,
                 admin_id: int = 401089055
                 ) -> Any:

        self.execute()

    # def __enter__(self):
    #     self.execute()

    def __exit__(self):
        self.application.stop()

    async def get_chat_id_from_tlg(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE
    ):
        chat_id = update.effective_chat.id

        await context.bot.send_message(
            chat_id=chat_id,
            text=f'{chat_id}')

    async def get_file_url(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE
    ):
        chat_id = update.effective_chat.id
        url = await get_url()
        await context.bot.send_message(
            chat_id=chat_id,
            text=f'{url}')

    async def get_chat_id(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE
    ):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'{update.effective_chat.id}')

    async def message_run_pol(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        message: str = 'Run Polling'
    ):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message)

    def command_chat_id(self):
        return CommandHandler('chat_id', self.get_chat_id)

    def command_chat(self):
        return CommandHandler('ch', self.get_chat_id_from_tlg)

    def command_get_file_u(self):
        return CommandHandler('export', self.get_file_url)

    def command_export_file(self):
        return CommandHandler(
            'export_file',
            management.call_command(
                'artefact_export_data_registry', chat_id=self.get_chat_id))

    async def post_stop(
        self,
        application: Application,
    ) -> None:
        await application.bot.send_message(401089055, "Shutting down...")

    async def post_init(self, application: Application) -> None:
        await application.bot.send_message(401089055, "Pull Started")

    def execute(self):
        self.application.add_handler(
            self.command_chat_id())
        self.application.add_handler(self.command_chat())

        self.application.add_handler(self.command_get_file_u())
        # self.application.post_init()
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
