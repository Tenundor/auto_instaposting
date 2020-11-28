from pathlib import Path
from pprint import pprint
import requests


def download_image(image_url, image_path):
    image_path = Path(image_path)
    Path(image_path.parent).mkdir(parents=True, exist_ok=True)
    response = requests.get(image_url)
    response.raise_for_status()
    image_path.write_bytes(
        response.content
    )


def fetch_spacex_launch_by_number(flight_number):
    spacex_url = 'https://api.spacexdata.com/v3/launches/past'
    spacex_response = requests.get(
        spacex_url,
        params={"flight_number": str(flight_number)}
    )
    spacex_response.raise_for_status()
    spacex_images_links = spacex_response.json()[0]["links"]["flickr_images"]
    for image_index, image_link in enumerate(spacex_images_links, start=1):
        filename = "./images/spacex_{0:03d}_launch_{1:03d}.jpg".format(flight_number, image_index)
        download_image(image_link, filename)

