import argparse
from instabot import Bot
from io import open
from pathlib import Path
from PIL import Image
import time


def change_file_extension_in_path(file_path, file_extension):
    file_path = Path(file_path)
    if file_path.match("*.{}".format(file_extension)):
        return file_path
    else:
        new_file_name = "{}.{}".format(file_path.stem, file_extension)
        return file_path.parent / new_file_name


def resize_image_for_instagram(image_sample):
    max_image_resolution = (1080, 1080)
    resized_image_copy = image_sample.copy()
    resized_image_copy.thumbnail(max_image_resolution)
    return resized_image_copy


def publish_images_to_instagram(
        username,
        password,
        images_dir,
        timeout,
):
    bot = Bot()
    bot.login(username=username, password=password)

    images = images_dir.glob("*.jpg")
    images = sorted(images)
    for image in images:
        image_name = Path(image).stem
        print("upload: " + image_name)
        bot.upload_photo(image, caption=image_name)
        time.sleep(timeout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скрипт публикует фотографии в заданном инстаграм-аккаунте")
    parser.add_argument("u", help="Имя пользователя")
    parser.add_argument("p", help="Пароль")
    args = parser.parse_args()

    images_dir = Path("images")

    for image_path in images_dir.glob("*.*"):
        with Image.open(image_path) as sample:
            sample = resize_image_for_instagram(sample)
            if sample.mode == "RGBA":
                sample = sample.convert("RGB")
            sample.save(image_path, format="JPEG")
        if not image_path.match("*.jpg"):
            image_path.replace(image_path.with_suffix(".jpg"))

    publish_images_to_instagram(
        username=args.u,
        password=args.p,
        images_dir=images_dir,
        timeout=10  # Images posted every 10 seconds
    )
