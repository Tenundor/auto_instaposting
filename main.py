from pathlib import Path
import requests


def download_file(file_url, file_path):
    file_path = Path(file_path)
    Path(file_path.parent).mkdir(parents=True, exist_ok=True)
    response = requests.get(file_url, verify=False)
    response.raise_for_status()
    file_path.write_bytes(
        response.content
    )


def fetch_spacex_last_launch():
    spacex_last_launch_url = 'https://api.spacexdata.com/v3/launches/latest'
    spacex_response = requests.get(spacex_last_launch_url)
    spacex_response.raise_for_status()
    spacex_json_content = spacex_response.json()
    flight_number = spacex_json_content["flight_number"]
    spacex_images_urls = spacex_json_content["links"]["flickr_images"]
    for spacex_image_index, spacex_image_url in enumerate(spacex_images_urls, start=1):
        filename = "./images/spacex_{0:03d}_launch_{1:03d}.jpg".format(flight_number, spacex_image_index)
        download_file(spacex_image_url, filename)


def fetch_spacex_launch_by_number(flight_number):
    spacex_url = 'https://api.spacexdata.com/v3/launches/past'
    spacex_response = requests.get(
        spacex_url,
        params={"flight_number": str(flight_number)}
    )
    spacex_response.raise_for_status()
    try:
        spacex_response_content = spacex_response.json()[0]
        spacex_images_links = spacex_response_content["links"]["flickr_images"]
        if not spacex_images_links:
            print("Couldn't find photos of the launch with flight number {}.".format(flight_number))
        else:
            for image_index, image_link in enumerate(spacex_images_links, start=1):
                filename = "./images/spacex_{0:03d}_launch_{1:03d}.jpg".format(flight_number, image_index)
                download_file(image_link, filename)
    except IndexError:
        print("Flight number {} not found".format(flight_number))


def get_file_extension_from_url(url):
    extension_index = url.rindex(".")
    return url[extension_index + 1:]


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
