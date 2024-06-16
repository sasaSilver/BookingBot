from aiogram.types import (KeyboardButton,
                           InlineKeyboardMarkup,
                           ReplyKeyboardMarkup,
                           InlineKeyboardButton, CallbackQuery)
from datetime import datetime
from calendar import monthrange
from utils import months_ru, DateCallback

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Создать бронь'),
            KeyboardButton(text='Удалить бронь'),
            KeyboardButton(text='Просмотреть календарь')
        ]
    ],
    resize_keyboard=True
)

def get_start_keyboard() -> ReplyKeyboardMarkup:
    return start_keyboard

def get_new_booking_calendar(date: datetime, user_id: int) -> InlineKeyboardMarkup:

    # days of the week row
    calendar_keyboard = [
        [InlineKeyboardButton(text=months_ru[date.month] + ' ' + str(date.year), callback_data='_')],
        list(map(
            lambda _day: InlineKeyboardButton(text=_day, callback_data='_'),
            ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        )),
    ]

    day_range: int = monthrange(date.year, date.month)[1]
    offset: int = date.weekday()

    # calculate number of rows needed
    rows = (offset + day_range) // 7 + ((offset + day_range) % 7 > 0)

    # placeholder buttons
    for i in range(rows):
        row: list[InlineKeyboardButton] = []
        for j in range(7):
            row.append(InlineKeyboardButton(text='­', callback_data='_'))
        calendar_keyboard.append(row)

    # calendar navigation buttons
    calendar_keyboard.append(
        [
            InlineKeyboardButton(text='<<', callback_data='page-prev'),
            InlineKeyboardButton(text='>>', callback_data='page-next')
        ],
    )
    now = datetime.now()

    # return empty past month
    if date.month < now.month:
        return InlineKeyboardMarkup(inline_keyboard=calendar_keyboard, resize_keyboard=True)
    # make all dates before now empty
    elif now.month == date.month:
        for i in range(now.day, day_range + 1):
            _row: int = (i + offset - 1) // 7 + 2
            _col: int = (i + offset - 1) % 7
            calendar_keyboard[_row][_col] = InlineKeyboardButton(
                text=str(i),
                callback_data=DateCallback(year=date.year, month=date.month, day=i, user_id=user_id).pack()
            )
        calendar_keyboard[(now.day + offset) // 7 + 2][(now.day + offset) % 7 - 1].text = f'[ {now.day} ]'
    # otherwise, fill in the whole month
    else:
        for i in range(date.day, day_range + 1):
            _row: int = (i + offset - 1) // 7 + 2
            _col: int = (i + offset - 1) % 7
            calendar_keyboard[_row][_col] = InlineKeyboardButton(text=str(i), callback_data=f'n-')

    return InlineKeyboardMarkup(inline_keyboard=calendar_keyboard, resize_keyboard=True)

