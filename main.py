import telebot
from config import TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = "Для получения курса валюты введите команду в формате:\n<имя валюты> <валюта, в которой хотите узнать цену> <количество>\n\n" \
           "Пример: USD RUB 100\n\n" \
           "Чтобы узнать доступные валюты, введите /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message):
    available_currencies = 'Доступные валюты для конвертации: \nUSD - Доллар \nEUR - Евро \nRUB - Рубль'
    bot.reply_to(message, available_currencies)

@bot.message_handler(content_types=['text'])
def get_currency(message):
    try:
        value = message.text.split(' ')
        if len(value) != 3:
            raise APIException('Неверное количество параметров.')

        base, quote, amount = value

        base = base.upper()
        quote = quote.upper()
        amount = float(amount)


        text = CurrencyConverter.get_price(base, quote, amount)
        bot.reply_to(message, text)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя: \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Непредвиденная ошибка: {e}')

if __name__ == '__main__':
    bot.polling(none_stop=True)
