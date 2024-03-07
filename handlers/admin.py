from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext      # Обработчик используется в "машине состояний".
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.deep_linking import get_start_link, decode_payload

from data_base import sql_db
from create_bot import dp, bot
from keyboards import button_case_admin


# +++++++++++++++++++++++++++++++++++++++++ Вспомогательные переменные +++++++++++++++++++++++++++++++++++++++++++++++++
ID = None
msg_controller = []

CHAT_TITLE = 'EGO Antibot portal'
PASSWORD = 'EGO5432P1234'
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# +++++++++++++++++++++++++++++++++++++++++ "Машины состояний" +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FSMLogin(StatesGroup):
    check_password = State()
    grant_access = State()
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# +++++++++++++++++++++++++++++++++++++++++ Получение прав модератора ++++++++++++++++++++++++++++++++++++++++++++++++++
# Начало проверки.
async def command_password_entering(message: types.Message):
    try:
        # print(message.chat.title, CHAT_TITLE, message.values)
        if message.chat.title != CHAT_TITLE:
            global msg_controller
            msg_controller = []

            msg_controller.append(await bot.send_message(message.from_user.id, 'Введи пароль:'))
            await FSMLogin.check_password.set()
    except Exception as ex:
        print('__error.admin.command_password_entering', ex)


# Проверка пароля.
async def password_checking(message: types.Message, state: FSMContext):
    try:
        msg_controller.append(message)

        if message.text.lower() == 'отмена':
            await bot.send_message(message.from_user.id, 'Ok.')
            await state.finish()   # Выход из режима "Машина состояний"

            for msg in msg_controller:
                await msg.delete()
            return

        if message.text == PASSWORD:
            global ID
            ID = message.from_user.id   # Предоставление прав модератора.
            print('* New moderator`s id=', ID)
            await bot.send_message(message.from_user.id, 'Что надо, хозяин?', reply_markup=button_case_admin)
            await state.finish()
            return

        msg_controller.append(await message.reply('Пароль неверный.'))
        await state.finish()

    except Exception as ex:
        print('__error.admin.password_checking', ex)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# +++++++++++++++++++++++++ Хендлер для проверки кол. реффералов +++++++++++++++++++++++++++++++++++++++++++++++++++++++
async def get_info(message: types.Message):
    try:
        if message.from_user.id == ID:
            results = await sql_db.get_info()  # Добавление очка Гриффиндору в БД.
            # print(results)

            charming_results = 'user_id: first_name: username: link_amount' + '\n'
            for person in results:
                for i, param in enumerate(person):
                    if i == 2:
                        charming_results += '@'
                    charming_results += str(param) + ': '
                charming_results += '\n'

            await bot.send_message(message.from_user.id, f"Баллы Участников:\n{charming_results}")
            await message.delete()
    except Exception as ex:
        print('__error.admin.get_info', ex)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# +++++++++++++++++++++++++ Хендлер для получения топ-200 +++++++++++++++++++++++++++++++++++++++++++++++++++++++
async def get_top_200(message: types.Message):
    try:
        if message.from_user.id == ID:
            results = await sql_db.get_top_200()  # Добавление очка Гриффиндору в БД.

            charming_results = 'user_id: first_name: username: link_amount' + '\n'
            for person in results:
                for i, param in enumerate(person):
                    if i == 2:
                        charming_results += '@'
                    charming_results += str(param) + ': '
                charming_results += '\n'

            await bot.send_message(message.from_user.id, f"Топ 200 самых активных участников:\n{charming_results}")
            await message.delete()
    except Exception as ex:
        print('__error.admin.get_top_200', ex)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




# +++++++++++++++++++++++++++++++++++++++++ Регистрация обработчиков +++++++++++++++++++++++++++++++++++++++++++++++++++
def register_handlers_admin(dp: Dispatcher):

    # Режим "Машины состояний" проверки валидности модератора.
    dp.register_message_handler(command_password_entering, commands=['moderator'], state=None)
    dp.register_message_handler(password_checking, state=FSMLogin.check_password)

    # Основные функции.
    dp.register_message_handler(get_info, commands=['info'])
    dp.register_message_handler(get_top_200, commands=['top'])

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
