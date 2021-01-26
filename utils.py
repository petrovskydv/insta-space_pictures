import glob
import logging
import os

import requests
from PIL import Image
from dotenv import load_dotenv
from instabot import Bot

logger = logging.getLogger(__name__)


def download_image(file_name, url, source_path, processed_images_path):
    response = requests.get(url, verify=False)
    response.raise_for_status()

    result_file_name = f'{file_name}{os.path.splitext(url)[1]}'
    file_path = os.path.join(source_path, result_file_name)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    logger.info(f'download file: {file_path}')

    image = Image.open(file_path)
    image.thumbnail((1080, 1080))
    image_path = os.path.join(processed_images_path, f'{file_name}.jpg')
    rgb_image = image.convert('RGB')
    rgb_image.save(image_path, format="JPEG")
    logger.info(f'save processed image: {image_path}')


def upload_images(folder_path):
    load_dotenv()
    instagram_username = os.getenv('INSTAGRAM_LOGIN')
    instagram_password = os.getenv('INSTAGRAM_PASSWORD')

    bot = Bot()
    bot.logger.setLevel(logging.ERROR)
    logger.info('bot start')
    bot.login(username=instagram_username, password=instagram_password)

    images_path = glob.glob(folder_path + "/*.jpg")
    images_path = sorted(images_path)
    for image_path in images_path:
        upload_result = bot.upload_photo(image_path, caption="Nice pic!")
        logger.info(f'upload result: {upload_result}')