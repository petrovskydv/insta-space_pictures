import glob
import logging
import os

from dotenv import load_dotenv
from instabot import Bot

logger = logging.getLogger(__name__)


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
