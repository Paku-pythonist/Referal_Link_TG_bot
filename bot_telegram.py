from aiogram import types
from aiogram.utils import executor   # Самостоятельный запуск бота.

from create_bot import dp, bot
from handlers import admin, client, other
from data_base import sql_db


# ++++++++++++++++++++++++++++++ Запуск БД ++++++++++++++++++++++++++++++
async def on_startup(_):
    sql_db.sql_start()
    print("Бот вышел в онлайн.")
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# ++++++++++++++++++++++++++++++++++ Добавление нового пользователя в группу +++++++++++++++++++++++++++++++++++++++++++
@dp.chat_join_request_handler()
async def command_user_welcome(update: types.ChatJoinRequest):
    # print('update.invite_link.name', update.invite_link.name, 'update.values', update.values)
    
    params = {}
    link_name = str(update.invite_link.name).split('||')
    try:
        params = {
            'creator_user_id': link_name[0],
            'creator_first_name': link_name[1] if link_name[1] else 'None',
            'creator_user_username': link_name[2] if link_name[2] else 'None',
            'invited_user_id': str(update.from_user.id),
            'invited_user_first_name': str(update.from_user.first_name),
            'invited_user_username': str(update.from_user.username) if update.from_user.username else 'None',
            'check': 'invited'
        }
        print('* command_user_welcome.params:', params)
    except Exception as ex:
        print('__error.command_user_welcome:', ex, '__error.params:', params)

    try:
        if update.from_user.is_bot: # or update.invite_link.creator.is_bot:   # Механизм выявления ботов.
            print('!_Выявлен бот. Новый пользователь будет добавлен, но балл не засчитан.')
        else:
            await sql_db.add_point(params)  # Добавление очка Гриффиндору в БД.

        params['check'] = 'invited'
        await sql_db.add_new_user(params)  # Запись в БД.

        await update.approve()   # Добавление нового пользователя.

    except Exception as ex:
        print(ex, 'bot_telegram.command_user_welcome')
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# ++++++++++++++++++++++++++++++++++ Приветствие нового пользователя +++++++++++++++++++++++++++++++++++++++++++++++++++
@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def new_chat_member(message: types.Message):
    for new_member in message.new_chat_members:
        href = "<a href='https://t.me/ego_paysenger_en'>Paysenger</a>"
        first_name = new_member.first_name if new_member.first_name != None else ''
        text = f"Hi {first_name} 👋\n" \
               f"Welcome to the official {href} Referral Bot.\n\n" \
               f"Press /get_referral_link to run the bot and get your referral link! \n\n" \
               f"roadmap \n\n" \
               f"/start /get_referral_link"
        try:
            await bot.send_message(message.from_user.id, text, parse_mode="HTML")
        except Exception as ex:
            await message.answer(text)
            print('* attention.new_chat_member.bot.send_message', ex)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# +++++++++++++++++++++++ Применение Обработчиков +++++++++++++++++++++++
admin.register_handlers_admin(dp)
client.register_handlers_client(dp)
# other.register_handlers_other(dp)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    except Exception as ex:
        print('__error.main:', ex)