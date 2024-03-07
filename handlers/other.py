import json, string

from aiogram import types, Dispatcher

from create_bot import dp
from data_base import sql_db


# # @dp.message_handler()
# async def echo_send(message: types.Message):
#     if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
#             .intersection(set(json.load(open('cenz.json', encoding='utf-8')))) != set():
#         await message.reply('Маты запрещены!')
#         await message.delete()
#     else:
#         await message.answer(message.text)
#
#
# def register_handlers_other(dp: Dispatcher):
#     dp.register_message_handler(echo_send)