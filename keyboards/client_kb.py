from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton('/start')
b2 = KeyboardButton('/get_referral_link')

button_case_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

button_case_client.row(b1, b2)   # .add(b1).insert(b2)