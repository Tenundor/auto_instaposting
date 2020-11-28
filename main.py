from pathlib import Path
import requests


def download_image(image_url, image_path):
    image_path = Path(image_path)
    Path(image_path.parent).mkdir(parents=True, exist_ok=True)
    response = requests.get(image_url)
    response.raise_for_status()
    image_path.write_bytes(
        response.content
    )


download_image('https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg', './images/hubble.jpeg')
