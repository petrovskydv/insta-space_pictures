import logging
import os

import urllib3
from dotenv import load_dotenv
from instabot import Bot

import fetch_hubble
import fetch_spacex
import utils


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

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

    instagram_bot = Bot()
    instagram_bot.logger.setLevel(logging.ERROR)
    instagram_bot.login(username=instagram_username, password=instagram_password)
    utils.upload_images(instagram_bot, processed_images_path)


if __name__ == '__main__':
    main()
