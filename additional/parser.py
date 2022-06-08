from bs4 import BeautifulSoup
from requests import cookies
from datetime import datetime
import fake_useragent
import requests
import json
import os

header = {
    'user-agent': fake_useragent.UserAgent().random
}

cookies = {
    'xnv2_currency_country': 'UA'
}

general_newsblock_link = 'https://www.xbox-now.com/ru/news'


def parse_game_dlc_links():
    response = requests.get(general_newsblock_link, headers=header, cookies=cookies)
    soup = BeautifulSoup(response.text, "lxml")

    search_news_blocks = soup.find('div', class_='news-entry-newstext')

    search_game_spoiler_panel = search_news_blocks.find_all('div', class_='panel-body')

    all_links_from_newsblock = []

    for tag_a in search_game_spoiler_panel:
        a = tag_a.find_all('a')
        for details in a:
            all_links_from_newsblock.append(details['href'])

    # print(all_links_from_newsblock)
    # print(len(all_links_from_newsblock))

    return all_links_from_newsblock


def parsing_names_prices_from_links():
    parsed_url = parse_game_dlc_links()
    #parsed_url = ['https://www.xbox-now.com/game/11978/aggelos']

    total_parsed_result = []
    count = 0

    for url in parsed_url:

        game_details = {}
        prices_dict = {}

        response = requests.post(url, headers=header, cookies=cookies)
        soup = BeautifulSoup(response.text, "lxml")

        game_name_on_page = soup.find_all('h2')[0].text.strip()
        game_details['game_name'] = game_name_on_page

        picture_url = soup.find(itemprop="image")['src']

        game_details['img'] = picture_url
        game_details['url'] = url

        prices_rows = soup.select('.col-xs-4.col-sm-3')

        for rows in prices_rows:
            try:
                if ' TRY' in rows.text.strip() or ' ARS' in rows.text.strip() or ' INR' in rows.text.strip():
                    if 'On Sale' in rows.text.strip() or 'с GOLD ' in rows.text.strip():
                        all_prices = rows.text.strip().replace(u'\xa0', u'').replace('\n', '').split(')')[1:]
                        low_price = all_prices[0].strip().split(' UAH')
                        prices_dict[float(low_price[0].strip())] = low_price[1]
                    elif 'Обычная цена' in rows.text.strip():
                        all_prices = rows.text.strip().replace(u'\xa0', u'').replace('\n', '').split('Обычная цена')[1:]
                        print(all_prices)
                        print(all_prices[0])
                        low_price = all_prices[0].strip().split(' UAH')
                        print(low_price)
                        print(low_price[0])
                        prices_dict[low_price[0].strip()] = low_price[1]
                    else:
                        all_prices = rows.text.strip().replace(u'\xa0', u'').replace('\n', '').split(')')
                        low_price = all_prices[0].strip().split(' UAH')
                        prices_dict[float(low_price[0].strip())] = low_price[1]

                    min_price = min(prices_dict.keys())
                    game_details['low_price'] = f'{min_price} UAH'
                    if ' TRY' in prices_dict.get(min_price):
                        game_details['region'] = 'Турция'
                    elif ' ARS' in prices_dict.get(min_price):
                        game_details['region'] = 'Аргентина'
                    elif ' INR' in prices_dict.get(min_price):
                        game_details['region'] = 'Индия'
            except IndexError:
                pass
            except ValueError:
                pass

        total_parsed_result.append(game_details)
        count += 1

        if count == 12:
            break

    print(f'TOTAL RESULT : {len(total_parsed_result)}')

    day_today = datetime.now().strftime('%d-%m-%Y')

    with open(f'{day_today}.json', 'w', encoding="utf-8") as file:
        json.dump(total_parsed_result, file, ensure_ascii=False)

    file_path = os.path.realpath(f'{day_today}.json')

    print(file_path)
    return file_path


parsing_names_prices_from_links()


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
