import asyncpg
from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types
from simple_print import sprint

from settings import DATABASE_URI_API
from settings import TELEGRAM_BOT_TOKEN


bot = Bot(token=TELEGRAM_BOT_TOKEN)
telegram_bot_dispatcher = Dispatcher(bot)


async def get_or_create_telegram_chat_id(message):

    conn = await asyncpg.connect(DATABASE_URI_API)
    user = None
    telegram_chat_id = message.chat["id"]

    try:
        sql_query = f'SELECT * FROM "user_profile_userprofile" LEFT JOIN "auth_user" ON "user_profile_userprofile"."user_id"="auth_user"."id" WHERE "user_profile_userprofile"."telegram_chat_id"=\'{telegram_chat_id}\';'
        user_profile = await conn.fetchrow(sql_query)
    except Exception as e:
        user_profile = None

    if user_profile:
        response = f"Вы уже подключены к нашей системе мониторинга. Ваше имя {user_profile['username']}. Ваш email {user_profile['email']}"
        response += f"\n\nЯ буду отправлять сюда уведомления в случае недоступности ваших серверов."
        response += f"\n\nС уважением бот 🖥️ мониторинга"
        await conn.close()
        return response

    try:
        sql_query = f'SELECT * FROM "user_profile_userprofile" LEFT JOIN "auth_user" ON "user_profile_userprofile"."user_id"="auth_user"."id" WHERE telegram_key=\'{message.text}\';'
        user_profile = await conn.fetchrow(sql_query)
    except Exception as e:
        user_profile = None

    if not user_profile:
        response = "Введите валидный ключ."
    else:
        sql_query = f"UPDATE \"user_profile_userprofile\" SET telegram_chat_id={telegram_chat_id} WHERE telegram_key='{message.text}';"
        user_profile = await conn.fetchrow(sql_query)
        response = "Вы успешно подключены к мониторингу."

    sprint(f"get_user_by_monitor_id user={user}", c="cyan", s=1, p=1)
    await conn.close()
    return response


@telegram_bot_dispatcher.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("@UnihotelMonitoringBot\nВ ответном сообщении напишите ваш ключ (Можно найти в «Изменить профайл/Уведомления»).")


@telegram_bot_dispatcher.message_handler()
async def echo(message: types.Message):
    sprint(message.chat, c="red")
    response = await get_or_create_telegram_chat_id(message)
    await message.answer(response)


if __name__ == "__main__":
    executor.start_polling(telegram_bot_dispatcher, skip_updates=True)
