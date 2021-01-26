import glob
import logging
import os

import requests
from PIL import Image
from instabot import Bot

logger = logging.getLogger(__name__)


def download_image(file_name, url, source_path):
    response = requests.get(url, verify=False)
    response.raise_for_status()

    result_file_name = f'{file_name}{os.path.splitext(url)[1]}'
    file_path = os.path.join(source_path, result_file_name)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    logger.info(f'download file: {file_path}')
    return file_path


def save_jpg_image(file_path, processed_images_path):
    image = Image.open(file_path)
    image.thumbnail((1080, 1080))
    file_name = os.path.splitext(os.path.split(file_path)[-1])[0]
    image_path = os.path.join(processed_images_path, f'{file_name}.jpg')
    rgb_image = image.convert('RGB')
    rgb_image.save(image_path, format="JPEG")
    logger.info(f'save processed image: {image_path}')


def upload_images(bot, folder_path):
    logger.info('bot start')
    images_path = glob.glob(f'{folder_path}/*.jpg')
    images_path = sorted(images_path)
    for image_path in images_path:
        logger.info(f'uploading a file {image_path}')
        upload_result = bot.upload_photo(image_path, caption="Nice pic!")
        logger.info(f'upload result: {upload_result}')
