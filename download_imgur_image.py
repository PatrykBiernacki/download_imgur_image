"""Program connects to Imgur API to download images from albums in default gallery."""

import os

import configparser
import imgurpython
import requests


def connect_to_imgur_api(config_file) -> imgurpython.ImgurClient:
    """Connect to IMGUR API. Pass config file containing client_id and client_secret for the app."""
    config = configparser.ConfigParser()
    config.read(config_file)
    client_id = config.get("credentials", "client_id")
    client_secret = config.get("credentials", "client_secret")
    client = imgurpython.ImgurClient(client_id, client_secret)
    return client


def _download_image(image: object, title: str) -> None:
    """Internal function to download images."""
    try:
        file_ext = image.link.split(".")[-1] if "." in [*image.link][-6:] else ""
        with open(
            os.path.join(os.getcwd(), "Gallery", f"{title[:20]}.{file_ext}"), "wb"
        ) as saved_image:
            saved_image.write(requests.get(image.link).content)
        print(f"downloaded {title}")
    except Exception as e:
        print(f"Exception {e}, passing {image.title}")
        pass


def download_all_images_from_gallery(
    client: imgurpython.ImgurClient,
    download_folder: str = os.path.join(os.getcwd(), "gallery"),
) -> None:
    """Downloads images available on main Imgur gallery. Assigns file extension. requires API connection. Can accept download directory."""
    items = client.gallery()
    os.makedirs(download_folder, exist_ok=True)
    no_name_images = 0
    for item in items:
        if not item.is_album:
            continue
        for image in client.get_album_images(album_id=item.id):
            if image.title:
                _download_image(image, image.title)
            else:
                no_name_images += 1
                _download_image(image, f"unnamed{no_name_images}")


if __name__ == "__main__":
    config_file = "settings.ini"
    client = connect_to_imgur_api(config_file)
    download_all_images_from_gallery(client)
