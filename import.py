import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import json
import traceback

TOKEN = "5622728594:AAElTQ4yJoHtEp-QCRRe173LAPKBi5Ftt5M"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Приветсвую, чтобы получить инструкцию введите /help, чтобы узнать о доступных валютах введите /values')
@bot.message_handler(commands=["help"])
def help(m, res=False):
    bot.send_message(m.chat.id, '1. Введите рубль\n2. Введите название валюты, в которую надо перевести\n3. Количество первоначальной валюты\nПример: рубль евро 100\nСписок доступных валют:/values')
@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in exchanges.keys():
        text = '\n' .join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров! Пример: рубль евро 100')
        
        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}\n Прочтите инструкцию /help" )
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}\n Прочтите инструкцию /help" )
    else:
        bot.reply_to(message,answer)


bot.polling(none_stop=True, interval=0)