import logging

import requests

import utils

logger = logging.getLogger(__name__)


def fetch_spacex_launch(source_path):
    logger.info('download SpaceX images')
    response = requests.get('https://api.spacexdata.com/v4/launches/5f8399fb818d8b59f5740d43')
    response.raise_for_status()
    review_result = response.json()
    picture_links = review_result['links']['flickr']['original']

    for picture_number, picture_link in enumerate(picture_links):
        file_name = 'spacex{}'.format(picture_number)
        logger.info(f'download {picture_link}')
        utils.download_image(file_name, picture_link, source_path)
