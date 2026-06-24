import requests

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)




TOKEN = "8635192224:AAEC26fL4i92GzNBlhi3MAJOW2FbVR1LIQI"


# получение курсов
def get_rates():

    url = "https://api.exchangerate-api.com/v4/latest/USD"

    data = requests.get(url).json()

    return {
        "USD": data["rates"]["USD"],
        "EUR": data["rates"]["EUR"],
        "RUB": data["rates"]["RUB"],
        "UZS": data["rates"]["UZS"]
    }


# кнопки
keyboard = [
    ["💵 Доллар", "💶 Евро"],
    ["₽ Рубль", "📊 Все курсы"]
]

markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)


# старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Выберите валюту:",
        reply_markup=markup
    )



# кнопки
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    rates = get_rates()

    usd = rates["UZS"]

    eur = rates["UZS"] / rates["EUR"]

    rub = rates["UZS"] / rates["RUB"]



    if text == "💵 Доллар":

        await update.message.reply_text(
f"""
💵 USD

1$ = {usd:,.0f} сум
100$ = {usd*100:,.0f} сум
1000$ = {usd*1000:,.0f} сум
10000$ = {usd*10000:,.0f} сум
"""
        )


    elif text == "💶 Евро":

        await update.message.reply_text(
f"""
💶 EUR

1€ = {eur:,.0f} сум
100€ = {eur*100:,.0f} сум
1000€ = {eur*1000:,.0f} сум
10000€ = {eur*10000:,.0f} сум
"""
        )


    elif text == "₽ Рубль":

        await update.message.reply_text(
f"""
₽ RUB

1₽ = {rub:.2f} сум
100₽ = {rub*100:.2f} сум
1000₽ = {rub*1000:.2f} сум
10000₽ = {rub*10000:.2f} сум
"""
        )


    elif text == "📊 Все курсы":

        await update.message.reply_text(
f"""
💵 Доллар

1$ = {usd:,.0f} сум
100$ = {usd*100:,.0f} сум
1000$ = {usd*1000:,.0f} сум
10000$ = {usd*10000:,.0f} сум


💶 Евро

1€ = {eur:,.0f} сум
100€ = {eur*100:,.0f} сум
1000€ = {eur*1000:,.0f} сум
10000€ = {eur*10000:,.0f} сум


₽ Рубль

1₽ = {rub:.2f} сум
100₽ = {rub*100:.2f} сум
1000₽ = {rub*1000:.2f} сум
10000₽ = {rub*10000:.2f} сум
"""
        )



# автообновление каждый день
async def update_rates():

    get_rates()

    print("Курсы обновлены")



app = Application.builder().token(TOKEN).build()


app.add_handler(
    CommandHandler("start", start)
)


app.add_handler(
    MessageHandler(filters.TEXT, buttons)
)












print("Бот запущен")
from flask import Flask
from threading import Thread

app_web = Flask(name)

@app_web.route("/")
def home():
    return "Converter bot is alive"

def run():
    app_web.run(host="0.0.0.0", port=8080)

Thread(target=run).start()

app.run_polling()
