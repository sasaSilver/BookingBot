import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from config_reader import config
from keyboards import get_start_keyboard, get_new_booking_calendar
from utils import get_other_month
import database

logging.basicConfig(level=logging.INFO)
bot = Bot(
    token=config.bot_token.get_secret_value(),
    parse_mode='MarkdownV2'
)
dp = Dispatcher()

async def on_startup(db):
    await database.db_start()


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('че надо', reply_markup=get_start_keyboard())


@dp.message(F.text == 'Создать бронь')
async def book_cmd(message: Message):
    await message.answer(text='Выбери день',
                         reply_markup=get_new_booking_calendar(datetime.now(), message.from_user.id))

@dp.callback_query(F.data.startswith('page-'))
async def change_calendar_page(query: types.CallbackQuery):
    cmd: str = query.data.split('-')[1]
    if cmd == 'prev':
        reply_markup = get_new_booking_calendar(get_other_month(-1), query.from_user.id)
    else:
        reply_markup = get_new_booking_calendar(get_other_month(1), query.from_user.id)
    await query.message.edit_reply_markup(reply_markup=reply_markup)


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, on_startup=on_startup, skip_updates=True)


asyncio.run(main())
