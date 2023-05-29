"""Program connects to Imgur API to download images from albums in default gallery."""

import os

import configparser
import imgurpython
import requests


class ImgurDlGallery:
    def __init__(self, client=None, read_albums=5) -> None:
        self.client = client
        self.read_albums = read_albums

    def connect_to_imgur_api(self, config_file) -> imgurpython.ImgurClient:
        """Connect to IMGUR API. Pass config file containing client_id and client_secret for the app."""
        try:
            config = configparser.ConfigParser()
            config.read(config_file)
            client_id = config.get("credentials", "client_id")
            client_secret = config.get("credentials", "client_secret")
            self.client = imgurpython.ImgurClient(client_id, client_secret)
        except:
            print(
                f"Improper credentials passed in config file. Pleae verify the config file: {config_file}."
            )
            input("Program will now close.")
            quit()
        try:
            self.read_albums = int(config.get("number of albums", "no_of_albums"))
        except:
            print(
                f"Config value for number of albums (no_of_albums) cannot be used. Pleae verify the config file: {config_file}."
            )
            input("Program will now close.")
            quit()
        return self.client

    def _download_image(self, image: object, title: str, download_folder: str) -> None:
        """Internal function to download images."""
        try:
            file_ext = image.link.split(".")[-1] if "." in [*image.link][-6:] else ""
            with open(
                os.path.join(download_folder, f"{title[:20]}.{file_ext}"), "wb"
            ) as saved_image:
                saved_image.write(requests.get(image.link).content)
            print(f"downloaded {title}")
        except Exception as e:
            print(f"Exception {e}, passing {image.title}")
            pass

    def download_all_images_from_gallery(
        self, download_folder: str = os.path.join(os.getcwd(), "gallery")
    ) -> None:
        """Downloads albums images available on main Imgur gallery. Assigns file extension. 
        Requires API connection. Can accept download directory."""
        items = self.client.gallery()
        os.makedirs(download_folder, exist_ok=True)
        no_name_images = 0
        for index_no, item in enumerate(items):
            # download number of albums specified in config file.
            if index_no > self.read_albums:
                break
            if not item.is_album:
                continue
            album_download_folder = os.path.join(
                download_folder, item.title[:35].strip()
            )
            os.makedirs(album_download_folder, exist_ok=True)
            for image in self.client.get_album_images(album_id=item.id):
                if image.title:
                    self._download_image(image, image.title, album_download_folder)
                else:
                    no_name_images += 1
                    self._download_image(
                        image, f"unnamed{no_name_images}", album_download_folder
                    )


if __name__ == "__main__":
    config_file = "settings.ini"
    client = ImgurDlGallery()
    client.connect_to_imgur_api(config_file)
    client.download_all_images_from_gallery()
