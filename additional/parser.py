from bs4 import BeautifulSoup
from requests import cookies
import fake_useragent
import requests
import re
import json
from datetime import datetime

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
    moy_spisok_co_vsemi_igrami = []

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
            find_price_from_header = re.findall('(\d+)', headers)
            most_little_price = ''.join(find_price_from_header[-1])

            # ищу картинку
            picture_url = soup.find(itemprop="image")['src']

            fully_game_details['game_name'] = game_name
            fully_game_details['img'] = picture_url
            fully_game_details['url'] = game_links

            prices_rows = soup.find_all(class_="col-xs-4 col-sm-3 col-md-2")
            prices_dict = {}

            for rows in prices_rows:
                try:
                    prices = rows.find_all('span')
                    prices_dict[prices[2].text.replace(u'\xa0', u'')] = prices[3].text.replace(u'\xa0', u'')
                    # all_prices_rows[prices[2].text.replace(' RUB','').replace(u'\xa0', u'')] = prices[3].text.replace(u'\xa0', u'')
                except IndexError:
                    pass

            for key, value in prices_dict.items():
                if most_little_price in key[:-3]:
                    if 'ARS' in value:
                        # print(f'Самая низкая цена в Аргентине -> {value}\nВ нашей валюте -> {key}')
                        fully_game_details['price'] = key
                    if 'TRY' in value:
                        # print(f'Самая низкая цена в Турции -> {value}\nВ нашей валюте -> {key}')
                        fully_game_details['price'] = key
            moy_spisok_co_vsemi_igrami.append(fully_game_details)
        except AttributeError as ae:
            print(ae)

    day_today = datetime.now().strftime('%d-%m-%Y')

    with open(f'price_{day_today}.json', 'w', encoding="utf-8") as file:
        json.dump(moy_spisok_co_vsemi_igrami, file, ensure_ascii=False)

def tested():
    general_news_link = 'https://www.xbox-now.com/ru/news'
    response = requests.get(general_news_link, headers=header, cookies=cookies)
    soup = BeautifulSoup(response.text, "lxml")
    news_entry_info = soup.find('div', class_='news-entry-info').find(itemprop="headline").text
    print(news_entry_info)

tested()