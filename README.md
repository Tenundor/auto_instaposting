# Публикация космических фотографий в Instagram

Программа автоматизирует скачивание фотографии из коллекций Hubble и SpaceX, а также их публикацию в вашем инcтаграм аккаунте.

## Установка

Скачайте код:
```
https://github.com/Tenundor/auto_instaposting
```
Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

## Скачивание фотографий

Для скачивания фотографий последнего запуска [SpaceX](https://www.spacex.com/) запустите `fetch_spacex.py`:
``` shell script
python fetch_spacex.py
```
Чтобы скачать подборку фотографий [Hubble](https://hubblesite.org/) запустите `fetch_hubble.py`:
``` shell script
python fetch_hubble.py
```
Фотографии сохраняются в папку `images` в директории с программой.

## Публикация фотографий

Запустите `post_images_instagram.py`, в качестве аргументов командной строки указав имя пользователя и пароль Instagram:
``` shell script
python post_images_instagram.py username password
```
## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](dvmn.org).
