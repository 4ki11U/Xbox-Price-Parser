from database_files.X_Database import XboxDB
from bs4 import BeautifulSoup
from requests import cookies
from datetime import datetime
import fake_useragent
import requests
import json
import os

xbox = XboxDB(r'D:\Python Projects\Xboxer-bot\database_files\xboxer_database.db')

user = fake_useragent.UserAgent().random

header = {
    'user-agent': user
}

cookies = {
    'xnv2_currency_country': 'UA'
}

general_newsblock_link = 'https://www.xbox-now.com/ru/news'


def parse_site_xbox_now(price_dictionary : dict):
    general_news_link = 'https://www.xbox-now.com/ru/news'
    response = requests.get(general_news_link, headers=header, cookies=cookies)
    soup = BeautifulSoup(response.text, "lxml")
    news_blocks = soup.find('div', class_='panel-body').find_all('a')
    # news_blocks = soup.find('div', class_='news-entry-newstext').find_all('a')

    all_game_links_from_newsblock = {}
    total_game_parsing_result = []

    for game_rows in news_blocks:
        if not 'Spoiler (expand)' in game_rows:
            links = game_rows['href']

            titles = game_rows['title']
            all_game_links_from_newsblock[titles] = links

    print(all_game_links_from_newsblock)

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
                    if ' TRY' in prices[3].text or ' ARS' in prices[3].text or ' INR' in prices[3].text:
                        uah_price = prices[2].text.replace(u'\xa0', u'').replace(' RUB', '').replace(' UAH',
                                                                                                     '').replace(',',
                                                                                                                 '')
                        uah_price_float = float(uah_price)
                        prices_dict[uah_price_float] = (prices[3].text.replace(u'\xa0', u''))
                except IndexError:
                    pass

            min_price = min(prices_dict)

            if ' TRY' in prices_dict.get(min_price):
                fully_game_details['region'] = 'Турция'
            elif ' ARS' in prices_dict.get(min_price):
                fully_game_details['region'] = 'Аргентина'
            elif ' INR' in prices_dict.get(min_price):
                fully_game_details['region'] = 'Индия'

            fully_game_details['price'] = f'{min_price} UAH'

            # print(fully_game_details)
            total_game_parsing_result.append(fully_game_details)
        except TypeError:
            print(TypeError)
        except ValueError:
            print(ValueError)

    print(len(total_game_parsing_result))

    day_today = datetime.now().strftime('%d-%m-%Y')

    with open(f'{day_today}.json', 'w', encoding="utf-8") as file:
        json.dump(total_game_parsing_result, file, ensure_ascii=False)

    file_path = os.path.realpath(f'{day_today}.json')

    print(file_path)

    return file_path


def games_parsing_in_newsblock():
    response = requests.get(general_newsblock_link, headers=header, cookies=cookies)
    soup = BeautifulSoup(response.text, "lxml")

    search_news_blocks = soup.find('div', class_='news-entry-newstext')

    search_game_spoiler_panel = search_news_blocks.find_all('div', class_='panel-body')

    print(search_game_spoiler_panel[0])

    games_links_from_newsblock = {}

    for tag_a in search_game_spoiler_panel:
        a = tag_a.find_all('a')
        for details in a:
            games_links_from_newsblock[details['title']] = details['href']

    return games_links_from_newsblock


def dlc_parsing_in_newsblock():
    response = requests.get(general_newsblock_link, headers=header, cookies=cookies)
    soup = BeautifulSoup(response.text, "lxml")
    news_blocks = soup.find('div', class_='news-entry-newstext')

    search_game_spoiler_panel = news_blocks.find_all('div', class_='panel-body')

    # print(search_game_spoiler_panel[1])

    dlc_links_from_newsblock = {}

    for tag_a in search_game_spoiler_panel:
        a = tag_a.find_all('a')
        for details in a:
            dlc_links_from_newsblock[details['title']] = details['href']

    return dlc_links_from_newsblock


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
