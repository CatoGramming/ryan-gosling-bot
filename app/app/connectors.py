import logging
from typing import Any
from telegram import Bot, Update
import asyncio
from typing import Callable
from app.settings import TELEGRAM_TOKEN

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    Application,
    CallbackQueryHandler
)
import time
from chadgpt.connectors import ChadGptService

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


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
            self.token).post_init(
                self.post_init).post_stop(
                self.post_stop).build()
        self.chat_id = chat_id
        self.admin_id = chat_id

    def __call__(
        self,
        admin_id: int = 401089055,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        self.execute()

    def __exit__(self):
        self.application.stop()

    async def start(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):
        if update.effective_chat.id != self.admin_id:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Вы не админ. Go away:)')
            return None

    async def inline_key(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:

        keyboard = [
            [
                InlineKeyboardButton(
                    'Анекдот про айти',
                    callback_data='it_joke'),
                InlineKeyboardButton(
                    'Анекдот про Райана Гослинга',
                    callback_data='gosling_joke'),
            ],
            [
                InlineKeyboardButton(
                    'Пожелание на Новый год',
                    callback_data='new_year'),
            ],
            [
                InlineKeyboardButton(
                    'Ничего не хочу!',
                    callback_data='Хорошо, вы ничего не хотите')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            'Что хотите?',
            reply_markup=reply_markup)

    async def get_new_year(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:

        keyboard = [
            [
                InlineKeyboardButton(
                    'Пожелание на Новый год',
                    callback_data='new_year'),
            ],
            [
                InlineKeyboardButton(
                    'Ничего не хочу!',
                    callback_data='Хорошо, вы ничего не хотите')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            'Привет! Нажми на кнопку, чтобы получить пожелание!',
            reply_markup=reply_markup)

    async def get_chat_id_from_tlg(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE
    ):
        chat_id = update.effective_chat.id

        await context.bot.send_message(
            chat_id=chat_id,
            text=f'{chat_id}')

    async def get_chat_id(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE
    ):
        if update.effective_chat.id != self.admin_id:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'NA. Ваш id или группы {update.effective_chat.id}')
            return None
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Ваш id или группы:\n{update.effective_chat.id}')

    async def message_run_pol(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        message: str = 'Run Polling'
    ):
        if update.effective_chat.id != self.admin_id:
            return None
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message)

    async def get_random_message(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
        # message: str
    ):
        if update.effective_chat.id != self.admin_id:
            return None
        chat_id = update.effective_chat.id
        message_id = update.message.message_id
        print(chat_id, message_id)

        print(update.message.message_id)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f'hello {message_id}')

    async def send_me_text(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):
        if update.effective_chat.id != self.admin_id:
            return None
        chat_id = update.effective_chat.id
        message_id = update.message.message_id
        print(chat_id, message_id)

        print(update.message.message_id)
        await context.bot.send_message(
            chat_id=chat_id,
            text='hello, send me text')

    async def get_test_edit_msg(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):
        if update.effective_chat.id != self.admin_id:
            return None
        chat_id = update.effective_chat.id
        message = await context.bot.send_message(
            chat_id=chat_id,
            text='Подождите, пожалуйста, запрос выполняется')

        time.sleep(10)
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=message.message_id,
            text='Прошло десять секунд. Сообщение изменено')

    async def get_response_from_chad(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        message: str = 'Привет'
    ):
        if update.effective_chat.id != self.admin_id:
            return None
        chat_id = update.effective_chat.id

        message = await context.bot.send_message(
            chat_id=chat_id,
            text='Подождите, пожалуйста, запрос выполняется')
        time.sleep(2)

        service = ChadGptService()
        chad_message = service.send_to_chad_gpt(
            message=message)
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message.message_id,
            text=chad_message)

    async def edit_message_text(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):
        if update.effective_chat.id != self.admin_id:
            return None
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=246,
            text='new_text')

    def command_chat_id(self):
        return CommandHandler('chat_id', self.get_chat_id)

    def command_chat(self):
        return CommandHandler('ch', self.get_chat_id_from_tlg)

    def command_get_file_u(self):
        return CommandHandler('export', self.get_file_url)

    def command_random_message(self):
        return CommandHandler('msg', self.get_random_message)

    def command_edit_message(self):
        return CommandHandler('edit_msg', self.edit_message_text)

    def command_new_year(self):
        return CommandHandler('new_year', self.get_new_year)

    def command_chad(self):
        return CommandHandler('chad', self.get_response_from_chad)

    def command_test_edit(self):
        return CommandHandler('test_edit', self.get_test_edit_msg)

    def command_start(self):
        return CommandHandler('start', self.start)

    async def post_stop(
        self,
        application: Application,
    ) -> None:
        await application.bot.send_message(401089055, 'Shutting down...')

    async def post_init(self, application: Application) -> None:
        await application.bot.send_message(401089055, 'Pull Started')

    async def button(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:

        query = update.callback_query

        await query.answer()

        await query.edit_message_text(text='Подождите, пожалуйста, запрос выполняется')
        time.sleep(2)
        data = {
            'it_joke': 'Расскажи анекдот про айти',
            'gosling_joke': 'Расскажи анекдот про Райана Гослинга',
            'new_year': 'Пожелай приятное на новый год',
        }

        service = ChadGptService()
        chad_message = service.send_to_chad_gpt(
            question=data[query.data])

        await query.edit_message_text(text=chad_message)

    async def help_command(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:

        await update.message.reply_text('Use /start to test this bot.')

    def execute(self):
        self.application.add_handler(
            self.command_chat_id())

        self.application.add_handler(self.command_start())
        self.application.add_handler(self.command_random_message())
        self.application.add_handler(self.command_edit_message())
        self.application.add_handler(self.command_chad())
        self.application.add_handler(self.command_test_edit())
        self.application.add_handler(
            CommandHandler('give_me_joke', self.inline_key))
        self.application.add_handler(
            CommandHandler('new_year', self.get_new_year))

        self.application.add_handler(CallbackQueryHandler(self.button))

        self.application.add_handler(CommandHandler('help', self.help_command))

        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
