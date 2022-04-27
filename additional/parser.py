import requests
from bs4 import BeautifulSoup

def parser():
    my_dict = dict()
    for number_page in range(1, 35):
        url = f'https://www.xbox-now.com/ru/recent-price-changes?page={number_page}'
        request = requests.get(url)
        soup = BeautifulSoup(request.text, "lxml")
        rows = soup.find_all("div", class_="box-body comparison-table-entry")
        for data in rows:
            game_name = data.find('strong').text.strip()
            game_price = (data.find('span')).text
            if '-100 %' in game_price:
                url_for_game = data.find(class_='pull-right').find('a')['href']
                my_dict[f'{game_name}'] = url_for_game
    return my_dict