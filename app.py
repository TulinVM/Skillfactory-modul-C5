#coding=UTF-8
import requests
import json
import telebot
from telebot import types

from config import exchanges, TOKEN
from extensions import ConversionException, Converter
import traceback


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Здравствуте.\nЯ помогу Вам ознакомиться с курсом валют.\n Для начала работы, введите мне команду в следующем формате:\n1.Имя валюты>\n2.В какую валюту перевести\n3.Количество переводимой валюты\nУвидеть список доступных валют: /values '
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\nНачать конвертацию: /convert\nВернуться к началу для ввода:/help '
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = 'Выберите валюту, из которой нужно конвертировать: '
    bot.send_message(message.chat.id, text, )
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text.strip().lower()
    text = 'Выберите валюту, в которую нужно конвертировать: '
    bot.send_message(message.chat.id, text, )
    bot.register_next_step_handler(message, sym_handler, base)

def sym_handler(message: telebot.types.Message, base):
    sym = message.text.strip().lower()
    text = 'Введите количество конвертируемой валюты: '
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, sym)

def amount_handler(message: telebot.types.Message, base, sym):
    amount = message.text.strip()
    try:
        new_price = Converter.get_price(base, sym, amount)
    except ConversionException as e:
        bot.send_message(message.chat.id, f"Извените это ошибка конвертации:\n{e}")
    else:
        text = f"Стоимость {amount} {base} в {sym} : {new_price}"
        bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')

    try:
        if len(values) != 3:
            raise ConversionException('Ошибка ввода пользователя (Неверное количество параметров!)')

        answer = Converter.get_price(*values)


    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e} \nПомощь:/help')
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        bot.reply_to(message, answer)


bot.polling()