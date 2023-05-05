import logging
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, CallbackQueryHandler
import aiohttp

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def bd(text_for_search: str):
    with sqlite3.connect('database.db') as connection:
        with connection.cursor() as cursor:
            cursor.execute("""

CREATE TABLE ads_table
(id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
price REAL)

""")

            query: str = """

SELECT id, title, price from ads_table
?
order by id DESC

"""
            cursor.execute(query, (text_for_search,))

    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        # todo Запрос для СОЗДАНИЯ ТАБЛИЦЫ
        query: str = """
CREATE TABLE ads_table
(id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
price REAL)
    """

        # todo Запрос для ВСТАВКИ СТРОКИ
        query: str = """
INSERT INTO ads_table (title, price) VALUES ('Бочка', '1500.5')
"""

        # todo Запрос для ВСТАВКИ СТРОКИ
        query: str = """
SELECT id, title, price FROM ads_table
"""
        cursor.execute(query)
        rows = cursor.fetchall()
        print(rows)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # with sqlite3.connect("database.db") as connection:
    #     cursor = connection.cursor()
    #     # todo Запрос для ИЗВЛЕЧЕНИЯ СТРОК
    #     query: str = """
    #     SELECT id, title, price FROM ads_table
    #     """
    #     cursor.execute(query)
    #     rows = cursor.fetchall()
    #     list1 = [f"({row[0]}) {row[1]} [{row[2]}]" for row in rows]
    # print(list1)
    list1 = ["Игрушка 1", "Игрушка 2", "Игрушка 3"]
    # data = requests.get("http://127.0.0.1:8000/api/ads/").json()
    # print(data)

    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/api/ads/') as response:
            ads = await response.json()
            list1 = [
                f"""({ad.get('id', 0)}) {ad.get('title', "")} [{ad.get('price', 0.0)}]"""
                for ad in ads
            ]

    keyboard = []
    for i in list1:
        new_button = [InlineKeyboardButton(i, callback_data=i)]
        keyboard.append(new_button)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите товар:', reply_markup=reply_markup)


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Введите часть названия или описания товара:')


async def search_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text

    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://127.0.0.1:8000/api/search/?text={text}') as response:
            ads = await response.json()
            list1 = [
                f"""({ad.get('id', 0)}) {ad.get('title', "")} [{ad.get('price', 0.0)}]"""
                for ad in ads
            ]

    keyboard = []
    for i in list1:
        new_button = [InlineKeyboardButton(i, callback_data=i)]
        keyboard.append(new_button)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите товар:', reply_markup=reply_markup)


async def button(update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Вы выбрали товар {query.data}")


def main():
    dispatcher = ApplicationBuilder().token('6019495776:AAE2vN___cjXK3hFn7IkcAwuZNARJtvhIro').build()

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('search', search))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_request))

    dispatcher.run_polling()


if __name__ == '__main__':
    main()  # todo START BOT
