import requests
import json


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float):
        currency_map = {
            "РУБЛЬ": "RUB",
            "ДОЛЛАР": "USD",
            "ЕВРО": "EUR"
        }

        keys = ["RUB", "USD", "EUR"]

        base = currency_map.get(base, base)
        quote = currency_map.get(quote, quote)
        try:
            r = requests.get(f'https://api.exchangerate-api.com/v4/latest/{base}')

            data = json.loads(r.content)
            if base not in keys:
                raise APIException(f"Валюта {base} не найдена.")

            if quote not in data['rates']:
                raise APIException(f"Валюта {quote} не найдена.")

            if r.status_code != 200:
                raise APIException(f"Ошибка получения данных: {r.status_code}")

            total_base = data['rates'][quote] * amount
            text = f'{amount:.2f} {base} = {total_base:.2f} {quote}'
            return text
        except Exception as e:
            return str(e)

