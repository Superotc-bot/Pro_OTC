import telebot
from tradingview_ta import TA_Handler, Interval
import os
from flask import Flask
from threading import Thread

# --- БЛОК ДЛЯ RENDER (чтобы не было ошибки портов) ---
app = Flask('')
@app.route('/')
def home(): return "Бот активен!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
# ---------------------------------------------------

TOKEN = '8629586982:AAG2lrWUHAC2uhaU9gYSdY99aStV4W1Ir-I'
bot = telebot.TeleBot(TOKEN)

def get_analysis(symbol):
    try:
        handler = TA_Handler(
            symbol=symbol, screener="forex", exchange="FX_IDC",
            interval=Interval.INTERVAL_5_MINUTES
        )
        analysis = handler.get_analysis()
        close, high, low = analysis.indicators['close'], analysis.indicators['high'], analysis.indicators['low']
        pivot = (high + low + close) / 3
        res1, sup1 = (2 * pivot) - low, (2 * pivot) - high
        return (f"💎 **АНАЛИЗ {symbol}**\n━━━━━━━━━━━━━━\n🎯 Сигнал: *{analysis.summary['RECOMMENDATION']}*\n\n"
                f"📈 Сопротивление: `{res1:.5f}`\n📉 Поддержка: `{sup1:.5f}`\n📍 Разворот: `{pivot:.5f}`")
    except: return "❌ Ошибка получения данных"

@bot.message_handler(content_types=['web_app_data'])
def web_app(message):
    bot.send_message(message.chat.id, get_analysis(message.web_app_data.data), parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🚀 Бот готов! Нажми АНАЛИЗ.")

if __name__ == "__main__":
    # Запускаем веб-сервер для порта в отдельном потоке
    Thread(target=run).start()
    # Запускаем самого бота
    bot.polling(none_stop=True)

