from download_file import download_file
import os
from pathlib import Path
import re
import requests


def fetch_hubble_image_by_id(image_id):
    hubble_image_url = "http://hubblesite.org/api/v3/image/{}".format(image_id)
    hubble_image_response = requests.get(hubble_image_url)
    hubble_image_response.raise_for_status()
    hubble_image_json_content = hubble_image_response.json()
    image_versions_description = hubble_image_json_content["image_files"]
    image_best_url = "http:{}".format(
        image_versions_description[-1]["file_url"]
    )
    image_file_extension = os.path.splitext(image_best_url)[1]
    image_name = hubble_image_json_content["name"]
    image_name = re.sub(r"[^\w\s\-\(\)]", "", image_name).strip()
    file_name = Path("images") / "{}{}".format(image_name, image_file_extension)
    download_file(image_best_url, file_name)


if __name__ == "__main__":
    hubble_get_parameters = {
        "page": "all",
        "collection_name": "printshop",
    }
    hubble_url = "http://hubblesite.org/api/v3/images"
    response_hubble_images_collection = requests.get(
        hubble_url,
        params=hubble_get_parameters,
    )
    response_hubble_images_collection.raise_for_status()
    hubble_images_collection = response_hubble_images_collection.json()
    amount_images = len(hubble_images_collection)
    for image_index, hubble_image_description in enumerate(hubble_images_collection, 1):
        image_id = hubble_image_description["id"]
        fetch_hubble_image_by_id(image_id)
        print("Downloaded", image_index, "images of", amount_images)
