from config import *

class TBExceptions(Exception):
    pass


class TelebotCurrency():

    def __init__(self):
        self.tb_token = TB_TOKEN

    @staticmethod
    def get_price(source, target, amount):

        a_source, n_source, a_target, n_target = TelebotCurrency.request_currency(source, target)
        print("get price")
        return a_source + a_target

    def text_checking(self, base, quote, amount):

        if base.upper() == quote.upper():
            raise TBExceptions("*Исходная и целевая валюты совпадают*\.")

#        print(base.upper(), "не в списке", base.upper() not in CURRENCY.keys())
#        print(base.lower(), "не в списке", base.lower() not in CURRENCY.values())

#        print(quote.upper(), "не в списке", quote.upper() not in CURRENCY.keys())
#        print(quote.lower(), "не в списке", quote.lower() not in CURRENCY.values())

        if base.upper() not in CURRENCY.keys() and base.lower() not in CURRENCY.values():
            raise TBExceptions("*Исходная валюта мне неизвестна*\.")

        if quote.upper() not in CURRENCY.keys() and quote.lower() not in CURRENCY.values():
            raise TBExceptions("*Целевая валюта мне неизвестна*\.")

        try:
            amount = float(amount)
        except ValueError:
            raise TBExceptions("*Не удалось обработать количество*\.")

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

        print(f"Запрашиваем {amount} {source} в {target}")
        return source, target

    @staticmethod
    def request_currency(source, target):
        a_source = 10
        a_target = 20

        #возвращает курсы source & target в пересчете к 100 рублям
        return a_source, n_source, a_target, n_target



