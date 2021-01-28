import logging

import requests

import utils

logger = logging.getLogger(__name__)


def fetch_spacex_launch(source_path, launch_id):
    logger.info('download SpaceX images')
    response = requests.get(f'https://api.spacexdata.com/v4/launches/{launch_id}')
    response.raise_for_status()
    review_result = response.json()
    picture_links = review_result['links']['flickr']['original']

    for picture_number, picture_link in enumerate(picture_links):
        file_name = f'spacex{picture_number}'
        logger.info(f'download {picture_link}')
        utils.download_image(file_name, picture_link, source_path)
