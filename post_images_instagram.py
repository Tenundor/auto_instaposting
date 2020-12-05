import glob
import sys
import os
import time
from io import open
from pathlib import Path
from PIL import Image


def prepare_image_for_instagram(original_image_path, processed_image_path):
    max_image_resolution = (1080, 1080)
    with Image.open(original_image_path) as sample:
        sample.thumbnail(max_image_resolution)
        if sample.mode == "RGBA":
            sample = sample.convert("RGB")
        sample.save(processed_image_path)


if __name__ == "__main__":
    images_dir = Path("images")
    processed_images_dir = images_dir.joinpath("./processed")
    processed_images_dir.mkdir(parents=True, exist_ok=True)
    for image_path in images_dir.glob("*.*"):
        new_image_path = processed_images_dir.joinpath(
            "./{}_resized.jpg".format(image_path.stem)
        )
        prepare_image_for_instagram(
            image_path,
            new_image_path,
        )
