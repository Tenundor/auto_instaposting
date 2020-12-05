from download_file import download_file
from get_extension import get_file_extension_from_url
from pathlib import Path
from PIL import Image
import requests


max_size = (1080, 1080)
for child in Path("images").iterdir():
    new_filename = "./resized/{}_resized.jpeg".format(child.stem)
    new_path = child.parent.joinpath(new_filename)
    Path(new_path.parent).mkdir(parents=True, exist_ok=True)
    with Image.open(child) as sample:
        sample.thumbnail(max_size)
        if sample.mode == "RGBA":
            sample = sample.convert("RGB")
        sample.save(new_path)
