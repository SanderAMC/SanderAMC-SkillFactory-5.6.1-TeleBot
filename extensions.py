from config import *
import redis
import requests
import json
from bs4 import BeautifulSoup

class TBExceptions(Exception):
    pass

class TBUserExceptions(TBExceptions):
    pass

class TelebotCurrency():

    def __init__(self):
        self.tb_token = TB_TOKEN
        self.red = redis.StrictRedis(
                host=RHOST,
                port=RPORT,
                password=RPASS,
                charset="utf-8",
                decode_responses=True
            )

    @staticmethod
    def logging(logstring):
        print(logstring)
        return

    @staticmethod
    def get_price(source, target, amount):

        a_rate, p_rate, n_source, n_target = TelebotCurrency.request_currency(source, target)
#        print(f"Исходная валюта: {n_source} Целевая валюта: {n_target}")
#        print(f"Курс пересчета {a_rate} Предыдущий курс {p_rate}")
        logstring = "тест строка для лога"
        TelebotCurrency.logging(logstring)
        return round(float(amount) * a_rate, 4), round(float(amount) * p_rate, 4), n_source, n_target

    def text_checking(self, base, quote, amount):

        if base.upper() == quote.upper():
            raise TBUserExceptions("*Исходная и целевая валюты совпадают*\.")

        if base.upper() not in CURRENCY.keys() and base.lower() not in CURRENCY.values():
            raise TBUserExceptions("*Исходная валюта мне неизвестна*\.")

        if quote.upper() not in CURRENCY.keys() and quote.lower() not in CURRENCY.values():
            raise TBUserExceptions("*Целевая валюта мне неизвестна*\.")

        try:
            amount = float(amount)
        except ValueError:
            raise TBUserExceptions("*Не удалось обработать количество*\.")

        if base.upper() in CURRENCY.keys():
            source = base.upper()
        else:
            for k, v in CURRENCY.items():
                if v == base.lower():
                    source = k

        if quote.upper() in CURRENCY.keys():
            target = quote.upper()
        else:
            for k, v in CURRENCY.items():
                if v == quote.lower():
                    target = k

        return source, target

    @staticmethod
    def request_currency(source, target):

        request = requests.get(CURRENCY_BASE)
        if request.status_code != 200:
            raise TBExceptions("*Нет доступа к серверу валют ЦБ\.*")

        cur_list = json.loads(BeautifulSoup(request.content, "lxml").text)

        if source == "RUB":
            n_source = "Российский рубль"
            a_nominator = 1
            p_nominator = 1
        else:
            a_source = cur_list["Valute"][source]["Value"]
            p_source = cur_list["Valute"][source]["Previous"]
            n_source = cur_list["Valute"][source]["Name"]
            a_nominator = a_source / cur_list["Valute"][source]["Nominal"]
            p_nominator = p_source / cur_list["Valute"][source]["Nominal"]

        if target == "RUB":
            n_target = "Российский рубль"
            a_denominator = 1
            p_denominator = 1
        else:
            a_target = cur_list["Valute"][target]["Value"]
            p_target = cur_list["Valute"][target]["Previous"]
            n_target = cur_list["Valute"][target]["Name"]
            a_denominator = a_target / cur_list["Valute"][target]["Nominal"]
            p_denominator = p_target / cur_list["Valute"][target]["Nominal"]

        a_rate = a_nominator / a_denominator
        p_rate = p_nominator / p_denominator

        return a_rate, p_rate, n_source, n_target



