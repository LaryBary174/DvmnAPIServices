import requests
import os
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token: str, url: str):
    api_url = 'https://api.vk.ru/method/utils.getShortLink'
    params = {'access_token': token, 'v': '5.199',
              'p1': 'v1',
              'url': url,
              'private': '0', }

    response = requests.post(url=api_url, params=params)
    response.raise_for_status()

    return response.json()['response']['short_url']


def count_clicks(token: str, short_url_key: str):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {'access_token': token, 'v': '5.199',
              'p1': 'v1',
              'key': short_url_key,
              'interval': 'forever',
              'extended': '0', }
    response = requests.post(url=api_url, params=params)
    response.raise_for_status()

    return response.json()['response']['stats']


def is_shorten_link(url):
    parser_url = urlparse(url)
    if parser_url.netloc == 'vk.cc' and parser_url.path != '':
        short_url_key = parser_url.path.lstrip('/')
        return short_url_key
    return False


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='Введите url')
    return parser


def main():
    load_dotenv()
    token = os.environ['VK_TOKEN']

    args = create_parser().parse_args()
    url = args.url
    short_url_key = is_shorten_link(url)
    try:
        if short_url_key:
            clicks_info = count_clicks(token, short_url_key)
            print('Инфа по кликам: ', clicks_info)
        else:
            short_link = shorten_link(token, url)
            print('Сокращенная ссылка: ', short_link)
    except requests.exceptions.RequestException as e:
        print(f'Ошибка в переданном URL {e}')
    except ValueError as e:
        print(f'Получен неверный тип данных {e}')
    except KeyError as e:
        print(f'Получен неверный ответ URL {e}')


if __name__ == '__main__':
    main()
