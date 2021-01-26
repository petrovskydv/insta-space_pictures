import logging
import os

import requests
import urllib3
from PIL import Image

import fetch_hubble
import fetch_spacex
import upload

PROCESSED_IMAGES_PATH = 'upload'
SOURCE_PATH = 'images'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def fetch_file_extension(file_link):
    return file_link.split('/')[-1].split('.')[-1]


def download_image(file_name, url):
    response = requests.get(url, verify=False)
    response.raise_for_status()

    result_file_name = f'{file_name}.{fetch_file_extension(url)}'
    file_path = os.path.join(SOURCE_PATH, result_file_name)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    logger.info(f'download file: {file_path}')

    image = Image.open(file_path)
    image.thumbnail((1080, 1080))
    image_path = os.path.join(PROCESSED_IMAGES_PATH, f'{file_name}.jpg')
    rgb_image = image.convert('RGB')
    rgb_image.save(image_path, format="JPEG")
    logger.info(f'save processed image: {image_path}')


def main():
    logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    hubble_logger = logging.getLogger('fetch_hubble')
    hubble_logger.setLevel(logging.INFO)
    spacex_logger = logging.getLogger('fetch_spacex')
    spacex_logger.setLevel(logging.INFO)
    upload_logger = logging.getLogger('upload')
    upload_logger.setLevel(logging.INFO)

    os.makedirs(SOURCE_PATH, exist_ok=True)
    os.makedirs(PROCESSED_IMAGES_PATH, exist_ok=True)

    urllib3.disable_warnings()
    fetch_spacex.fetch_spacex_launch()
    fetch_hubble.fetch_hubble_images_from_collection('spacecraft')
    upload.upload_images(PROCESSED_IMAGES_PATH)


if __name__ == '__main__':
    main()
