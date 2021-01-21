import logging
import os
from pprint import pprint

import requests

logger = logging.getLogger(__name__)


def main():
    file_name = 'hubble.jpeg'
    url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    destination_path = 'images'
    os.makedirs(destination_path, exist_ok=True)
    result_filepath = os.path.join(destination_path, file_name)

    download_image(result_filepath, url)


def download_image(file_path, url):
    response = requests.get(url)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def fetch_spacex_launch():
    response = requests.get('https://api.spacexdata.com/v4/launches/5f8399fb818d8b59f5740d43')
    response.raise_for_status()
    review_result = response.json()
    picture_links = review_result['links']['flickr']['original']

    destination_path = 'images'
    os.makedirs(destination_path, exist_ok=True)

    for picture_number, picture_link in enumerate(picture_links):
        result_filename = 'spacex{}.jpg'.format(picture_number)
        result_filepath = os.path.join(destination_path, result_filename)
        logger.info(f'download {picture_link}')
        download_image(result_filepath, picture_link)


def hubble():
    response = requests.get('http://hubblesite.org/api/v3/image/1')
    response.raise_for_status()
    review_result = response.json()
    image_details = review_result['image_files']
    pprint(image_details)
    for image in image_details:
        pprint(image['file_url'].split('/')[-1])


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger.setLevel(logging.INFO)

    # main()
    # fetch_spacex_launch()
    hubble()