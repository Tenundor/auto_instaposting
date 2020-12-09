import argparse
from instabot import Bot
from io import open
from pathlib import Path
from PIL import Image
import time


def change_file_extension_in_path(file_path, file_extension):
    if file_path.match("*.{}".format(file_extension)):
        return file_path
    else:
        new_file_name = "{}.{}".format(file_path.stem, file_extension)
        return file_path.parent / new_file_name


def prepare_image_for_instagram(image_sample):
    max_image_resolution = (1080, 1080)
    resized_image = image_sample.copy().thumbnail(max_image_resolution)
    if resized_image.mode == "RGBA":
        resized_image = resized_image.convert("RGB")
    return resized_image


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Скрипт публикует фотографии в заданном инстаграм-аккаунте"
    )
    parser.add_argument("u", help="Имя пользователя")
    parser.add_argument("p", help="Пароль")
    args = parser.parse_args()

    images_dir = Path("images")
    for image_path in images_dir.glob("*.*"):
        if image_path.match("*.REMOVE_ME"):
            continue
        new_image_path = change_file_extension_in_path(image_path, "jpg")
        with Image.open(image_path) as sample:
            sample = prepare_image_for_instagram(sample)
            sample.save(new_image_path)

    posted_images_list = []
    try:
        with open("images.txt", "r", encoding="utf8") as f:
            posted_images_list = [
                Path(x) for x in f.read().splitlines()
            ]
    except Exception:
        posted_images_list = []

    timeout = 10  # pics will be posted every 10 seconds

    bot = Bot()  # Оформи как отдельную функцию (пользователь, пароль, директория с фотографиями, таймаут, posted_images list
    bot.login(username=args.u, password=args.p)  # Отдели ввод-вывод от обработки. Можно сделать return список файлов
# Которые нужно занести в текстовый документ
    while True:
        images = images_dir.glob("*.jpg")
        images = sorted(images)
        try:
            for image in images:
                if image in posted_images_list:
                    continue

                image_name = Path(image).stem

                print("upload: " + image_name)

                bot.upload_photo(image, caption=image_name)
                if bot.api.last_response.status_code != 200:
                    print(bot.api.last_response)
                    break

                if image not in posted_images_list:
                    posted_images_list.append(image)  # add image to posted images list
                    with open("images.txt", "a", encoding="utf8") as f:
                        f.write(str(image) + "\n")

                time.sleep(timeout)

        except Exception as e:
            print(str(e))
        time.sleep(60)
