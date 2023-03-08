import time
import os

import argparse

from src import client
from src import wallpaper

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ClientAPI Arguments')
    parser.add_argument('ip', type=str, help='IP address of server')
    parser.add_argument('timer', type=int, help='Time interval for API requests in seconds')
    parser.add_argument('--image_folder', type=str, default="wallpaper", help='Folder to save images')
    parser.add_argument('--save_as', type=str, default='image', help='Specify a custom image name prefix, example: "image"')
    args = parser.parse_args()

    # Create an instance of ClientAPI using the parsed arguments
    api = client.ClientAPI(args.ip, args.timer, args.image_folder, args.save_as)

    while True:
        time.sleep(api.SLEEP_TIME)
        api.delete_image()
        api.download_image()
        wallpaper.Wallpaper.set_wallpaper(os.path.abspath(os.path.join(api.image_folder, api.IMAGE_NAME)))