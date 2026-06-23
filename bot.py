import requests
import json

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)


TOKEN= "8635192224:AAEC26fL4i92GzNBlhi3MAJOW2FbVR1LIQI"


# Получаем курсы
def get_rates():

    url = "https://api.exchangerate-api.com/v4/latest/USD"

    data = requests.get(url).json()

    return {
        "USD": 1,
        "EUR": data["rates"]["EUR"],
        "RUB": data["rates"]["RUB"],
        "UZS": data["rates"]["UZS"]
    }



# Кнопки
keyboard = [
    ["💵 Доллар", "💶 Евро"],
    ["₽ Рубль", "📊 Все курсы"]
]

markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)



# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Выберите валюту:",
        reply_markup=markup
    )



# Нажатия кнопок
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    rates = get_rates()


    if text == "💵 Доллар":

        await update.message.reply_text(
            f"💵 1 USD = {rates['UZS']} сум"
        )


    elif text == "💶 Евро":

        euro = rates["UZS"] / rates["EUR"]

        await update.message.reply_text(
            f"💶 1 EUR = {round(euro)} сум"
        )


    elif text == "₽ Рубль":

        rub = rates["UZS"] / rates["RUB"]

        await update.message.reply_text(
            f"₽ 1 RUB = {round(rub,2)} сум"
        )


    elif text == "📊 Все курсы":

        euro = rates["UZS"] / rates["EUR"]
        rub = rates["UZS"] / rates["RUB"]

        await update.message.reply_text(
            f"""
💵 USD
1 доллар = {rates['UZS']} сум

💶 EUR
1 евро = {round(euro)} сум

₽ RUB
1 рубль = {round(rub,2)} сум
"""
        )



app = Application.builder().token(TOKEN).build()


app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    MessageHandler(filters.TEXT, buttons)
)


print("Бот запущен")

app.run_polling()