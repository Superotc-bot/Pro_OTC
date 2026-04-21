import telebot
from tradingview_ta import TA_Handler, Interval

# Твой личный токен
TOKEN = '8629586982:AAG2lrWUHAC2uhaU9gYSdY99aStV4W1Ir-I'
bot = telebot.TeleBot(TOKEN)

def get_analysis(symbol):
    try:
        # Анализируем 5-минутный таймфрейм для точности
        handler = TA_Handler(
            symbol=symbol,
            screener="forex",
            exchange="FX_IDC",
            interval=Interval.INTERVAL_5_MINUTES
        )
        analysis = handler.get_analysis()
        
        # Данные для уровней
        close = analysis.indicators['close']
        high = analysis.indicators['high']
        low = analysis.indicators['low']
        
        # Расчет классических уровней Pivot
        pivot = (high + low + close) / 3
        res1 = (2 * pivot) - low  # Сопротивление
        sup1 = (2 * pivot) - high # Поддержка
        
        rec = analysis.summary['RECOMMENDATION']
        
        text = (
            f"💎 **АНАЛИЗ {symbol} (5m)**\n"
            f"━━━━━━━━━━━━━━\n"
            f"🎯 Сигнал: *{rec}*\n\n"
            f"📈 Сопротивление: `{res1:.5f}`\n"
            f"📉 Поддержка: `{sup1:.5f}`\n"
            f"📍 Точка разворота: `{pivot:.5f}`\n"
            f"━━━━━━━━━━━━━━\n"
            f"💡 *Совет: открывайте сделку, когда цена касается уровня поддержки или сопротивления.*"
        )
        return text
    except:
        return "❌ Ошибка данных. Попробуйте позже."

@bot.message_handler(content_types=['web_app_data'])
def web_app(message):
    pair = message.web_app_data.data
    result = get_analysis(pair)
    bot.send_message(message.chat.id, result, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🚀 Бот активирован! Нажми кнопку АНАЛИЗ в меню.")

bot.polling(none_stop=True)
