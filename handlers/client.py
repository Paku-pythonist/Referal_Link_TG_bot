from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.deep_linking import get_start_link, decode_payload
from aiogram.utils.markdown import link

from data_base import sql_db
from create_bot import dp, bot
from keyboards import button_case_client
from data import config


# +++++++++++++++++++++++++ Хендлер для приветствия новобранца и расшифровки ссылки ++++++++++++++++++++++++++++++++++++
async def command_start(message: types.Message):
    try:
        href = "<a href='https://t.me/ego_paysenger_en'>Paysenger</a>"
        first_name = message.from_user.first_name if message.from_user.first_name else ''
        text = f"Hi {first_name} 👋\n" \
               f"Welcome to the official {href} Referral Bot.\n\n" \
               f"Press /get_referral_link to run the bot and get your referral link! \n\n" \
               f"roadmap /start /get_referral_link"

        await bot.send_message(message.from_user.id, text, reply_markup=button_case_client, parse_mode="HTML")
        await message.delete()
    except Exception as ex:
        print('__error.client.command_start',ex)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# +++++++++++++++++++++++++++++++++++++ Хендлер для создания ссылок ++++++++++++++++++++++++++++++++++++++++++++++++++++
async def get_ref(message: types.Message):
    CHAT_ID = config['CHAT_ID']
    try:
        # link = "https://t.me/+Irm1_HymxVcwYTFi" + "?start=" + str(message.from_user.id)   # Ссылка на группу.
        link_name = str(message.from_user.id) + '||' + str(message.from_user.first_name) + '||' + str(message.from_user.username)
        link = await bot.create_chat_invite_link(CHAT_ID, name=link_name, creates_join_request=True)
        link = link.invite_link

        first_name = message.from_user.first_name if message.from_user.first_name != None else ''
        dog_first_name = ('@' + first_name) if first_name != '' else ''

        text = f"{link} {first_name} your referral link for the contest is here.\n" \
               f"Invite your friends and get in the leaderboard to secure rewards!\n" \
               f"🚀\n" \
               f"{dog_first_name}"

        await message.answer(text, parse_mode="HTML")
        await message.delete()
        print('Выдана реф. ссылка id=', str(message.from_user.id))
    except Exception as ex:
        print('__error.client.get_ref',ex)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# +++++++++++++++++++++++++++++++++++++++++ Регистрация обработчиков +++++++++++++++++++++++++++++++++++++++++++++++++++
def register_handlers_client(dp: Dispatcher):

    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(get_ref, commands=['get_referral_link'])
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

