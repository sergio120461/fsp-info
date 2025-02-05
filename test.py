import feedparser
import requests
from bs4 import BeautifulSoup

def read_rss_feed(rss_url):
    """
    Загружает, разбирает и "читает" RSS-ленту, выводя основную информацию.

    Args:
        rss_url: URL-адрес RSS-ленты.
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

        print(f"Название канала: {feed.channel.title}")
        print(f"Ссылка на канал: {feed.channel.link}")
        print(f"Описание канала: {feed.channel.description}")

        print("\n--- Записи в ленте ---")

        i = 0

        for entry in feed.entries:
            i += 1
            print(i)
            if i>10 :
                return None
            print("-" * 20)
            print(f"Заголовок: {entry.title}")
            print(f"Ссылка: {entry.link}")

            # Проверяем, есть ли описание и выводим его
            print(f"Description: {entry.description}")
            
            if hasattr(entry, 'description'):
                # Используем BeautifulSoup, если описание содержит HTML
                description_soup = BeautifulSoup(entry.description, 'html.parser')

                print(f"Description_soup: {description_soup}")

                print(f"Описание: {description_soup.get_text()}")
            else:
                print("Описание отсутствует")

            if hasattr(entry, 'pubDate'):
                print(f"Дата публикации: {entry.pubDate}")
            else:
                 print("Дата публикации отсутствует")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке RSS-ленты: {e}")
        return None
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return None


if __name__ == "__main__":
    rss_url = "https://zakupki.gov.ru/tinyurl/94e19d9ef34138e9686ffb45dd622016f48a989e21de00dfc070ba11521f4b94"  # Замените на нужный URL
    read_rss_feed(rss_url)