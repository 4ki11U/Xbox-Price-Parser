from database_files.X_Database import XboxDB
from bs4 import BeautifulSoup
from requests import cookies
from datetime import datetime
import fake_useragent
import requests
import json
import re

import os

xbox = XboxDB(r'D:\Python Projects\Xboxer-bot\database_files\xboxer_database.db')

user = fake_useragent.UserAgent().random

header = {
    'user-agent': user
}

cookies = {
    'xnv2_currency_country': 'UA'
}


def parse_site_xbox_now():
    general_news_link = 'https://www.xbox-now.com/ru/news'
    response = requests.get(general_news_link, headers=header, cookies=cookies)
    soup = BeautifulSoup(response.text, "lxml")
    news_blocks = soup.find('div', class_='panel-body').find_all('a')

    all_game_links_from_newsblock = {}
    total_game_parsing_result = []

    for rows in news_blocks:
        titles = rows['title']
        links = rows['href']
        all_game_links_from_newsblock[titles] = links

    for game_name, game_links in all_game_links_from_newsblock.items():
        try:
            fully_game_details = {}

            response = requests.get(game_links, headers=header, cookies=cookies)
            soup = BeautifulSoup(response.text, "lxml")
            headers = soup.find(class_="content-header").find('h1').text

            picture_url = soup.find(itemprop="image")['src']

            fully_game_details['game_name'] = game_name
            fully_game_details['img'] = picture_url
            fully_game_details['url'] = game_links

            prices_rows = soup.find_all(class_="col-xs-4 col-sm-3 col-md-2")

            prices_dict = {}
            global uah_price_float

            for rows in prices_rows:
                try:
                    prices = rows.find_all('span')
                    # print(prices)
                    # print(prices[2].text)
                    # print(prices[3].text)
                    # print('#'*10)
                    if ' TRY' in prices[3].text or ' ARS' in prices[3].text or ' INR' in prices[3].text:
                        uah_price = prices[2].text.replace(u'\xa0', u'').replace(' RUB', '').replace(' UAH',u'').replace(',','')
                        # uah_price = prices[0].text.replace(u'\xa0', u'').replace(' UAH', u'').replace(',','')
                        uah_price_float = float(uah_price)
                        prices_dict[uah_price_float] = (prices[3].text.replace(u'\xa0', u''))
                except IndexError:
                    pass

            # print(prices_dict)

            min_price = min(prices_dict)

            if ' TRY' in prices_dict.get(min_price):
                fully_game_details['region'] = 'Турция'
            elif ' ARS' in prices_dict.get(min_price):
                fully_game_details['region'] = 'Аргентина'
            elif ' INR' in prices_dict.get(min_price):
                fully_game_details['region'] = 'Индия'

            fully_game_details['price'] = f'{min_price} UAH'

            print(fully_game_details)
            total_game_parsing_result.append(fully_game_details)
        except TypeError as te:
            print(te)
        except ValueError as ve:
            print(ve)

    print(len(total_game_parsing_result))

    day_today = datetime.now().strftime('%d-%m-%Y')

    with open(f'{day_today}.json', 'w', encoding="utf-8") as file:
        json.dump(total_game_parsing_result, file, ensure_ascii=False)

    file_path = os.path.realpath(f'{day_today}.json')

    print(file_path)

    return file_path


def search_new_deals():
    general_news_link = 'https://www.xbox-now.com/ru/news'
    response = requests.get(general_news_link, headers=header, cookies=cookies)
    soup = BeautifulSoup(response.text, "lxml")

    news_entry_infoname = soup.find('div', class_='news-entry-info').find(itemprop="headline").text
    last_deals_news_fromdb = xbox.select_deals_details()

    if not news_entry_infoname == last_deals_news_fromdb[-1][0]:
        inert_last_deals = xbox.insert_deals_details(news_entry_infoname)
        return True
    else:
        print('No new news, nothing to parse')
        return False
