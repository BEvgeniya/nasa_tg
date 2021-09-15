import os
import time
from os import listdir
from urllib.parse import urlparse

import telegram
import requests
import datetime


def load_picture(url, path, params=None):
    headers = {
        'User-Agent': 'curl',
        'Accept-Language': 'ru-RU'
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    with open(path, 'wb') as file:
        return file.write(response.content)


def fetch_spacex_last_launch(folder):
    os.makedirs(folder, exist_ok=True)
    spacex_url = 'https://api.spacexdata.com/v4/launches/latest'
    response = requests.get(spacex_url)
    response.raise_for_status()
    launch = response.json()
    spacex_image_links = launch['links']['flickr']['original']

    if spacex_image_links:
        for index, image_url in enumerate(spacex_image_links):
            filename = f'{folder}/space{index}.jpg'
            load_picture(image_url, filename)


def get_nasa_day_pictures(folder, nasa_api_token):
    params = {
        'api_key': nasa_api_token,
        'count': 30
    }
    os.makedirs(folder, exist_ok=True)
    url = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(url, params=params)
    response.raise_for_status()
    image_urls = []

    for nasa_image in response.json():
        try:
            image_urls.append(nasa_image['hdurl'])
        except KeyError:
            image_urls.append(nasa_image['url'])

    for index, image_url in enumerate(image_urls):
        extension = get_file_extension(image_url)
        if extension:
            filename = f'{folder}/nasa_day{index}{extension}'
            load_picture(image_url, filename)


def get_file_extension(url):
    parsed_url = urlparse(url)
    parsed_url_path = parsed_url.path
    extension = os.path.splitext(parsed_url_path)[1]
    return extension


def get_nasa_epic_pictures(folder, nasa_api_token):
    os.makedirs(folder, exist_ok=True)
    params = {
        'api_key': nasa_api_token
    }
    url = f'https://api.nasa.gov/EPIC/api/natural'
    response = requests.get(url, params=params)
    response.raise_for_status()

    for index, image in enumerate(response.json()):
        image_name = image['image']
        image_date = datetime.datetime.fromisoformat(image['date'])
        base_url = 'https://api.nasa.gov/EPIC/archive/natural/'\
            f'{image_date.strftime("%x")}/png/{image_name}.png'
        path = f'{folder}/planet{index}.png'
        load_picture(base_url, path, params)


def post_photos(all_folders, bot, chat_id):
    while True:
        for folder in all_folders:
            for file in listdir(folder):
                time.sleep(60 * 60 * 24)
                with open(f'{folder}/{file}', 'rb') as document:
                    bot.send_document(chat_id=chat_id, document=document)


def main():
    nasa_api_token = os.environ['NASA_API_TOKEN']
    tg_bot_token = os.environ['TG_BOT_TOKEN']
    bot = telegram.Bot(token=tg_bot_token)
    all_folders = ['earth_epic_photos', 'images', 'nasa_dayly']
    chat_id = os.environ['TG_CHAT_ID']
    get_nasa_day_pictures(all_folders[2], nasa_api_token)
    get_nasa_epic_pictures(all_folders[0], nasa_api_token)
    fetch_spacex_last_launch(all_folders[1])
    post_photos(all_folders, bot, chat_id)

if __name__ == '__main__':
    main()
