import os
import time
from os import listdir
from urllib.parse import urlparse

import telegram
import requests
import datetime


def loadpicture(url, path):
    headers = {
        'User-Agent': 'curl',
        'Accept-Language': 'ru-RU'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    with open(path, 'wb') as file:
        return file.write(response.content)


def fetch_spacex_last_launch():
    spacex_url = 'https://api.spacexdata.com/v4/launches'
    response = requests.get(spacex_url)
    response.raise_for_status()
    launches = response.json()
    for launch in launches:
        spacex_image_links = launch['links']['flickr']['original']
        if spacex_image_links != []:
            for index, image_url in enumerate(spacex_image_links):
                filename = 'images/space' + str(index) + '.jpg'
                loadpicture(image_url, filename)


def get_nasa_day_pictures(nasa_apitoken):
    params = {
        'count': 30
    }

    url = f'https://api.nasa.gov/planetary/apod?api_key={nasa_apitoken}'
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
        if extension != '':
            filename = 'nasa_dayly/nasa_day' + str(index) + extension
            loadpicture(image_url, filename)


def get_file_extension(url):
    parsed_url = urlparse(url)
    parsed_url_path = parsed_url.path
    splitted_path = os.path.split(parsed_url_path)[1]
    extension = os.path.splitext(splitted_path)[1]
    return extension


def get_correct_data(date_str):
    image_date = datetime.datetime.fromisoformat(date_str)
    year = image_date.year
    month = image_date.month
    day = image_date.day
    if month < 10:
        month = '0' + str(month)
    if day < 10:
        day = '0' + str(day)
    return [str(year), month, day]


def get_nasa_epic_pictures(nasa_apitoken):
    url = f'https://api.nasa.gov/EPIC/api/natural?api_key={nasa_apitoken}'
    response = requests.get(url)
    response.raise_for_status()

    for index, image_info in enumerate(response.json()):
        image_name = image_info['image']
        image_date = get_correct_data(image_info['date'])

        base_url = f'https://api.nasa.gov/EPIC/archive/natural/{image_date[0]}/{image_date[1]}/{image_date[2]}/png/{image_name}.png?api_key={nasa_apitoken}'

        path = 'earth_epic_photos/planet' + str(index) + '.png'
        loadpicture(base_url, path)


def main():
    nasa_apitoken = os.environ['NASA_APITOKEN']
    tg_bot_token = os.environ['TG_BOT_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']
    bot = telegram.Bot(token=tg_bot_token)

    while True:
        all_folders = ['earth_epic_photos', 'images', 'nasa_dayly']
        for folder in all_folders:
            for file in listdir(folder):
                time.sleep(10)
                bot.send_document(chat_id=chat_id,
                                  document=open(folder + '/' + file, 'rb'))


if __name__ == '__main__':
    main()
