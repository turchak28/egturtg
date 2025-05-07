
import requests
import json

class APIException(Exception):
    """Пользовательское исключение для ошибок API."""
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        """
        Конвертирует валюту через API и возвращает результат.
        :param base: Валюта для конвертации (например, USD)
        :param quote: Валюта, в которую конвертируем (например, EUR)
        :param amount: Количество валюты
        :return: Результат конвертации
        """
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{base.upper()}"
            response = requests.get(url)
            data = json.loads(response.text)
            
            if quote.upper() not in data["rates"]:
                raise APIException(f"Валюта {quote} не найдена.")
            
            rate = data["rates"][quote.upper()]
            return round(rate * amount, 2)
        
        except requests.exceptions.RequestException:
            raise APIException("Ошибка при запросе к API.")
        except json.JSONDecodeError:
            raise APIException("Ошибка при обработке данных API.")