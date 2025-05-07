import telebot
from telebot import types
from config import TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

# Доступные валюты
CURRENCIES = {
    "доллар": "USD",
    "евро": "EUR",
    "рубль": "RUB"
}

@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    instructions = (
        "💱 *Конвертер валют* 💱\n\n"
        "🔹 Формат запроса:\n"
        "`<валюта1> <валюта2> <количество>`\n\n"
        "🔹 Пример:\n"
        "`доллар рубль 100`\n\n"
        "🔹 Доступные команды:\n"
        "`/values` — список доступных валют\n"
        "`/help` — справка"
    )
    bot.send_message(message.chat.id, instructions, parse_mode="Markdown")

@bot.message_handler(commands=['values'])
def send_currencies(message):
    currencies_text = "📊 *Доступные валюты:*\n"
    for name, code in CURRENCIES.items():
        currencies_text += f"• {name.capitalize()} ({code})\n"
    bot.send_message(message.chat.id, currencies_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            raise APIException("Неверный формат. Используйте: <валюта1> <валюта2> <количество>")
        
        base, quote, amount = parts
        amount = float(amount)
        
        if base.lower() not in CURRENCIES:
            raise APIException(f"Валюта {base} не поддерживается.")
        if quote.lower() not in CURRENCIES:
            raise APIException(f"Валюта {quote} не поддерживается.")
        
        base_code = CURRENCIES[base.lower()]
        quote_code = CURRENCIES[quote.lower()]
        
        result = CurrencyConverter.get_price(base_code, quote_code, amount)
        bot.reply_to(message, f"💵 {amount} {base_code} = {result} {quote_code}")
    
    except ValueError:
        bot.reply_to(message, "❌ Ошибка: количество должно быть числом.")
    except APIException as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Неизвестная ошибка: {str(e)}")

if __name__ == "__main__":
    bot.polling(none_stop=True)