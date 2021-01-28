import logging

import requests

import utils

logger = logging.getLogger(__name__)


def fetch_hubble_images_from_collection(collection_name, source_path):
    logger.info(f'download Hubble images from collection {collection_name}')
    response = requests.get(f'http://hubblesite.org/api/v3/images/{collection_name}')
    response.raise_for_status()
    images = response.json()
    for image in images:
        fetch_hubble_image(image['id'], source_path)


def fetch_hubble_image(image_id, source_path):
    response = requests.get(f'http://hubblesite.org/api/v3/image/{image_id}')
    response.raise_for_status()
    review_result = response.json()
    image_details = review_result['image_files']
    file_link = image_details[-1]['file_url']
    logger.info(f'download http:{file_link}')
    utils.download_image(image_id, f'http:{file_link}', source_path)
