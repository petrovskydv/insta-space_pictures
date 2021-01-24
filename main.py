import logging
import os

import requests
import urllib3
from PIL import Image

import fetch_hubble
import fetch_spacex
import upload

PROCESSED_IMAGES_PATH = 'upload'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def fetch_file_path(file_name, source_path):
    os.makedirs(source_path, exist_ok=True)
    result_filepath = os.path.join(source_path, file_name)
    return result_filepath


def fetch_file_extension(file_link):
    return file_link.split('/')[-1].split('.')[-1]


def download_image(file_name, url):
    response = requests.get(url, verify=False)
    response.raise_for_status()

    source_path = 'images'
    result_file_name = f'{file_name}.{fetch_file_extension(url)}'
    file_path = fetch_file_path(result_file_name, source_path)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    logger.info(f'download file: {file_path}')

    image = Image.open(file_path)
    image.thumbnail((1080, 1080))
    image_path = fetch_file_path(f'{file_name}.jpg', PROCESSED_IMAGES_PATH)
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

    urllib3.disable_warnings()
    fetch_spacex.fetch_spacex_launch()
    fetch_hubble.fetch_hubble_images_from_collection('spacecraft')
    upload.upload_images(PROCESSED_IMAGES_PATH)


if __name__ == '__main__':
    main()
