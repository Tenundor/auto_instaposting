import argparse
import glob
import sys
import os
import time
from io import open
from pathlib import Path
from PIL import Image
# sys.path.append(os.path.join(sys.path[0], "../../"))
from instabot import Bot


def prepare_image_for_instagram(original_image_path, processed_image_path):
    max_image_resolution = (1080, 1080)
    with Image.open(original_image_path) as sample:
        sample.thumbnail(max_image_resolution)
        if sample.mode == "RGBA":
            sample = sample.convert("RGB")
        sample.save(processed_image_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Скрипт публикует фотографии в заданном инстаграм-аккаунте"
    )
    parser.add_argument("u", help="Имя пользователя")
    parser.add_argument("p", help="Пароль")
    args = parser.parse_args()
    images_dir = Path("images")
    processed_images_dir = images_dir.joinpath("./processed")
    processed_images_dir.mkdir(parents=True, exist_ok=True)
    for image_path in images_dir.glob("*.*"):
        new_image_path = processed_images_dir.joinpath(
            "./{}.jpg".format(image_path.stem)
        )
        prepare_image_for_instagram(
            image_path,
            new_image_path,
        )

    posted_pic_list = []
    try:
        with open("pics.txt", "r", encoding="utf8") as f:
            posted_pic_list = f.read().splitlines()
    except Exception:
        posted_pic_list = []

    print(posted_pic_list)

    timeout = 20  # pics will be posted every 20 seconds

    bot = Bot()
    bot.login(username=args.u, password=args.p)

    while True:
        pics = processed_images_dir.glob("*.jpg")
        pics = sorted(pics)
        try:
            for pic in pics:
                if pic_string in posted_pic_list:
                    continue

                pic_name = Path(pic).stem

                print("upload: " + pic_name)

                bot.upload_photo(pic, caption=pic_name.replace("-", " "))
                if bot.api.last_response.status_code != 200:
                    print(bot.api.last_response)
                    break

                if pic_string not in posted_pic_list:
                    posted_pic_list.append(pic_string)
                    with open("pics.txt", "a", encoding="utf8") as f:
                        f.write(pic_string + "\n")

                time.sleep(timeout)

        except Exception as e:
            print(str(e))
        time.sleep(60)
