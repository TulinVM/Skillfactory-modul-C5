#coding=UTF-8
import requests
import json

from config import exchanges


class ConversionException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise ConversionException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise ConversionException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise ConversionException(f'Невозможно перевести одинаковые валюты {base}! \nНачать заново: /help')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise ConversionException(f'Не удалось обработать количество {amount}!')




        r = requests.get(f"https://v6.exchangerate-api.com/v6/eebab05275eaf8f4066a58e2/pair/{base_key}/{sym_key}")
        #r = requests.get('https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={sym_key}')

        #resp = json.loads(r.content)[keys[base]]
        resp = json.loads(r.content)
        new_price = resp['conversion_rate'] * amount
        # text = f"Цена {amount} {base} в {sym} : {new_price}"
        return new_price
