from datetime import datetime

from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from dateutil.relativedelta import relativedelta

curr_month = datetime(datetime.now().year, datetime.now().month, 1)


def get_other_month(offset: int) -> datetime:
    global curr_month
    other_month = curr_month + relativedelta(months=offset)
    curr_month = other_month
    return other_month

class DateCallback(CallbackData, prefix='date', sep='-'):
    year: int
    month: int
    day: int
    user_id: int

months_ru = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь'
}
