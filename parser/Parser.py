import os
from datetime import datetime
from loguru import logger
from bs4 import BeautifulSoup
from notifiers import get_notifier
from urllib.request import urlopen
from notifiers.logging import NotificationHandler


class Parser:
    def __init__(self) -> None:
        self.params = {
            "token": os.getenv("RASASI_BOT_TOKEN"),
            "chat_id": int(os.getenv(f"MY_CHAT_ID")),
            "parse_mode": "html"
        }
        
        
        handler = NotificationHandler('telegram', defaults=self.params)
        logger.add(handler, level="INFO")
        logger.info(f'\n\n\U0001F9FE <b><i>Start cwis \n{datetime.now()}</i></b>')
        self.telegram = get_notifier('telegram')

        self.list_cities = {
            'Ангарск': 'https://angarsk.shinapoint.ru/catalog/tires/search/w-165/h-65/r-14/leto/',
            'Братск': 'https://bratsk.shinapoint.ru/catalog/tires/search/w-165/h-65/r-14/leto/',
            'Владивосток': 'https://vladivostok.shinapoint.ru/catalog/tires/search/w-165/h-65/r-14/leto/',
            'Иркутск': 'https://shinapoint.ru/catalog/tires/search/w-165/h-65/r-14/leto/',
            'Улан-Уде': 'https://ulan-ude.shinapoint.ru/catalog/tires/search/w-165/h-65/r-14/leto/',
            'Усть-Илимск': 'https://ust-ilimsk.shinapoint.ru/catalog/tires/search/w-165/h-65/r-14/leto/',
            'Усть-Кут': 'https://ust-kut.shinapoint.ru/catalog/tires/search/w-165/h-65/r-14/leto/',
            'Хабаровск': 'https://khabarovsk.shinapoint.ru/catalog/tires/search/w-165/h-65/r-14/leto/',
            'Чита': 'https://chita.shinapoint.ru/catalog/tires/search/w-165/h-65/r-14/leto/',
            'Красноярск': 'https://krasnoyarsk.shinapoint.ru/catalog/tires/search/w-165/h-65/r-14/leto/',
        }



    def check_wheels_in_stock(self):
        # 1. Зайти на сайт
        for city, site in self.list_cities.items():
            html = urlopen(site)
            html = html.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            wheels_list = soup.find_all('div', ['item_block col-4 col-md-3 col-sm-6 col-xs-6'])

            msg = f'<a href="{site}">{city}</a>\n\n'
            send_city_report = False
            for wheel in wheels_list:
                title = wheel.find('div', ['item-title'])
                stock = wheel.find('div', ['item-stock'])
                in_stock = stock.find('a', ['fast_show_stores'])
                if in_stock:
                    send_city_report = True
                    price = wheel.find('span', ['price_value'])
                    # price = ''
                    msg += f'<i>{title.text.strip()}</i>\n<b>{in_stock.text.strip()}</b>\n{price.text.strip()} руб.\n\n'

            if send_city_report: self.telegram.notify(message=msg, **self.params)



if __name__ == '__main__':
    p = Parser()
    p.check_wheels_in_stock()