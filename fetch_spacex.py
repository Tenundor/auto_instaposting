from download_file import download_file
from get_extension import get_file_extension_from_url
import requests


def fetch_spacex_last_launch():
    spacex_last_launch_url = "https://api.spacexdata.com/v3/launches/latest"
    spacex_response = requests.get(spacex_last_launch_url)
    spacex_response.raise_for_status()
    spacex_json_content = spacex_response.json()
    flight_number = spacex_json_content["flight_number"]
    spacex_images_urls = spacex_json_content["links"]["flickr_images"]
    for spacex_image_index, spacex_image_url in enumerate(spacex_images_urls, start=1):
        image_file_extension = get_file_extension_from_url(spacex_image_url)
        filename = "./images/spacex_{0:03d}_launch_{1:03d}.{2:s}".format(
            flight_number,
            spacex_image_index,
            image_file_extension,
        )
        download_file(spacex_image_url, filename)


if __name__ == "__main__":
    fetch_spacex_last_launch()
