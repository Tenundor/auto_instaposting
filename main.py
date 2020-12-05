from download_file import download_file
from get_extension import get_file_extension_from_url
from pathlib import Path
from PIL import Image
import requests


def fetch_hubble_image_by_id(image_id):
    hubble_image_url = 'http://hubblesite.org/api/v3/image/{}'.format(image_id)
    hubble_image_response = requests.get(hubble_image_url)
    hubble_image_response.raise_for_status()
    hubble_image_json_content = hubble_image_response.json()
    image_versions_description = hubble_image_json_content["image_files"]
    image_best_url = "http:{}".format(
        image_versions_description[-1]["file_url"]
    )
    image_file_extension = get_file_extension_from_url(image_best_url)
    file_name = "./images/{}.{}".format(image_id, image_file_extension)
    download_file(image_best_url, file_name)


hubble_get_parameters = {
    "page": "all",
    "collection_name": "wallpaper",
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
