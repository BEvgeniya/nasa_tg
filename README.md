# Telegram channel Space-Photos

Программа, скачивающая фотографии космоса (Nasa APOD, Nasa EPIC, API Spacex) и выгружающая их в телеграм канал с определенной периодичностью.


## Environment


### Requirements


Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть есть конфликт с Python2) для установки зависимостей:
1) requests
2) telegram

А также токен Nasa API и API-токен Telegram Bot (можно получить у @BotFather).

```bash
pip install -r requirements.txt
```


### Environment variables

- NASA_APITOKEN
- TG_BOT_TOKEN
- TG_CHAT_ID
 
 
#### How to get

NASA_APITOKEN - Зарегистрируйтесь на [nasa api](https://api.nasa.gov/ "nasa api") и получите уникальный api-ключ.
TG_BOT_TOKEN - Создайте телеграм бота у @BotFather и получите уникальный токен.
TG_CHAT_ID - Создайте телеграм канал, затем напишите сообщение в канал и перешлите его в @getmyid_bot, чтобы узнать id вашего канала.


## Run

Запускается на Linux(Python 3) или Windows.
