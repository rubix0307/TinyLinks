import asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from telebot import types

from common import create_short_url, get_long_url, get_all_user_url
from config import BOT_TOKEN


bot = AsyncTeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
async def send_welcome(message: Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Мои ссылки', callback_data='my_links'))

    await bot.send_photo(
        message.chat.id,
        photo='https://www.seobility.net/en/wiki/images/5/54/Social-Sharing.png',
        caption="ㅤ\nСоздавайте короткие ссылки\nПоделитесь ими где угодно\nㅤ",
    )


@bot.message_handler(commands=['get'])
async def get_long(message: Message):
    short_url = ''.join(message.text.split('/get')[-1:]).strip()

    if short_url:
        long_url_data = await get_long_url(short_url)

        if 'long_url' in long_url_data:
            await bot.send_message(message.chat.id,text=f'{long_url_data["long_url"]}')
        else:
            await bot.send_message(message.chat.id,text=long_url_data["error"])
    else:
        await bot.send_message(message.chat.id, text=f'Укажите короткую ссылку\n/get короткая_ссылка')

@bot.message_handler(commands=['get_all'])
async def get_all(message: Message):
        all_links = await get_all_user_url(message.from_user.id)
        links_as_a = [f'''<a href='{link["long_url"]}'>{link["long_url"]}</a>''' for link in all_links]
        a_as_str = "\n".join(links_as_a)
        await bot.send_message(message.chat.id, text=f'Все ссылки:\n{a_as_str}', parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
@bot.message_handler(commands=['create'])
async def create_short(message: Message):
    url = ''.join(message.text.split('/create')[-1:]).strip()

    if url:
        custom_short_url = None
        short_url_data = await create_short_url(url, custom_short_url=custom_short_url, user_id=message.from_user.id)

        if 'short_url' in short_url_data:
            await bot.send_message(message.chat.id,text=f'Ссылка успешно сохранена\nhttp://localhost/{short_url_data["short_url"]}')
        else:
            await bot.send_message(message.chat.id,text=f'Произошла ошибка\nhttp://localhost/{short_url_data["error"]}')


asyncio.run(bot.polling())
