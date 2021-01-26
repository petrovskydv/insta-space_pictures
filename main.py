import logging
import os

import urllib3
from dotenv import load_dotenv

import fetch_hubble
import fetch_spacex
import utils


def main():
    logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    hubble_logger = logging.getLogger('fetch_hubble')
    hubble_logger.setLevel(logging.INFO)
    spacex_logger = logging.getLogger('fetch_spacex')
    spacex_logger.setLevel(logging.INFO)
    upload_logger = logging.getLogger('utils')
    upload_logger.setLevel(logging.INFO)

    processed_images_path = 'upload'
    source_path = 'images'
    collection_name = 'spacecraft'

    os.makedirs(processed_images_path, exist_ok=True)
    os.makedirs(source_path, exist_ok=True)

    urllib3.disable_warnings()
    fetch_spacex.fetch_spacex_launch(source_path, processed_images_path)
    fetch_hubble.fetch_hubble_images_from_collection(collection_name, source_path, processed_images_path)

    load_dotenv()
    instagram_username = os.getenv('INSTAGRAM_LOGIN')
    instagram_password = os.getenv('INSTAGRAM_PASSWORD')
    utils.upload_images(processed_images_path, instagram_username, instagram_password)


if __name__ == '__main__':
    main()
