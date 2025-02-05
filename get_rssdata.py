import feedparser
import requests
from bs4 import BeautifulSoup
import re
from collections import OrderedDict

def read_rss_feed(rss_url):
    """
    Загружает, разбирает и "читает" RSS-ленту, выводя основную информацию.
    Args:         rss_url: URL-адрес RSS-ленты.
    """

    try:
        headers =   {
                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                    }
        response = requests.get(rss_url, headers=headers)

        response.raise_for_status() #Проверка ответа HTTP

        feed = feedparser.parse(response.content)

        if feed.bozo:
            print(f"Ошибка парсинга RSS-ленты: {feed.bozo_exception}")
            return None

        print("\n--- Записи в ленте ---")

        souplist = []
        for entry in feed.entries:
            if hasattr(entry, 'description'):
            # Используем BeautifulSoup, если описание содержит HTML
                description_soup = BeautifulSoup(entry.description, 'html.parser')
                souplist.append(description_soup)

        else:
            print("Описание отсутствует")
            #souplist.append("Описание отсутствует")
    
        return souplist

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке RSS-ленты: {e}")
        return None
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return None


def parse_string_with_tokens(text, tokens):

    """
    Парсит строку по списку токенов.

    Args:
        text: Строка для парсинга.
        tokens: Список токенов (ключевых слов) для поиска.

    Returns:
        OrderedDict, содержащий пары "токен: значение".
    """
    result = dict()
    for i, token in enumerate(tokens):
        # Шаблон для поиска токена и следующего за ним значения
        if i < len(tokens) -1 :
            pattern = re.compile(rf"{re.escape(token)}:\s*(.*?)(?={re.escape(tokens[i+1])}|\Z)", re.DOTALL)
        else:
          pattern = re.compile(rf"{re.escape(token)}:\s*(.*?)\Z", re.DOTALL)

        match = pattern.search(text)

        if match:
            value = match.group(1).strip()
            result[token] = value
        else:
           result[token] = None

    return result



if __name__ == "__main__":
    rss_url = "https://zakupki.gov.ru/tinyurl/94e19d9ef34138e9686ffb45dd622016f48a989e21de00dfc070ba11521f4b94"  # 

    rss_records = read_rss_feed(rss_url)
    
    tokens = ['Description', 'Найденный результат','Наименование объекта закупки','Размещение выполняется по',
          'Наименование Заказчика', 'Начальная цена контракта', 'Валюта','Размещено', 'Обновлено', 'Этап размещения',
          'Идентификационный код закупки (ИКЗ)']
    print(f'len(rss_records) = {len(rss_records)} ')

    tenders = dict()
    #print()
    for rss_record in rss_records:
        #print(rss_record)
        d={}
        #soup = BeautifulSoup(rss_record, 'html.parser')
        soup = rss_record
        link_href = soup.find('a')['href']
        d['link'] = link_href
        #print(f"link: {d['link']}")
        #print()

        parsed_data = parse_string_with_tokens(soup.get_text(), tokens)
        for key, value in parsed_data.items():
            #print(f"{key}: {value}")
            #print()
            d[key]=value

        tenders[d["Идентификационный код закупки (ИКЗ)"]] = d
        


        break
    print(tenders)
'''
    a = read_rss_feed(rss_url)
    print(f'len(a) = {len(a)} ')
    print(f'type a[1]   {type(a[1])}')
    for i in range(3):
        print()
        print(a[i])
'''