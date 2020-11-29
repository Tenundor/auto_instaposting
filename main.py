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


def fetch_spacex_last_launch():
    spacex_last_launch_url = 'https://api.spacexdata.com/v3/launches/latest'
    spacex_response = requests.get(spacex_last_launch_url)
    spacex_response.raise_for_status()
    spacex_response_content = spacex_response.json()
    flight_number = spacex_response_content["flight_number"]
    spacex_images_links = spacex_response_content["links"]["flickr_images"]
    if not spacex_images_links:
        print("Couldn't find photos of the last launch.")
    else:
        for image_index, image_link in enumerate(spacex_images_links, start=1):
            filename = "./images/spacex_{0:03d}_launch_{1:03d}.jpg".format(flight_number, image_index)
            download_image(image_link, filename)


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
                download_image(image_link, filename)
    except IndexError:
        print("Flight number {} not found".format(flight_number))


def get_file_extension_from_url(url):
    extension_index = url.rfind(".")
    return url[extension_index + 1:]


hubble_first_image_url = 'http://hubblesite.org/api/v3/image/1'
hubble_response = requests.get(hubble_first_image_url, verify=False)
hubble_response.raise_for_status()
hubble_response_content = hubble_response.json()
hubble_image_files_url = hubble_response_content["image_files"]
for image_file in hubble_image_files_url:
    print(image_file["file_url"])

print(get_file_extension_from_url("http://abc.xom/api/image/mmm.pdf"))
