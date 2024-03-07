from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button_info = KeyboardButton('/info')
button_top = KeyboardButton('/top')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

button_case_admin.row(button_top, button_info)
