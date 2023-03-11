import time
import os

import argparse
import requests

from src import client
from scripts import wallpaper

def mainloop(api: client.ClientAPI):
    '''Function to call to ClientAPI every X seconds, and set downloaded image as wallpaper'''
    def download_image_retry():
        '''Retries to connect to the api after SLEEP_TIME, if it couldn't'''
        try:
            api.download_image()
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            time.sleep(api.SLEEP_TIME)
            download_image_retry()

    while True:
        time.sleep(api.SLEEP_TIME)
        api.delete_image()        
        download_image_retry()
        wallpaper.Wallpaper.set_wallpaper(os.path.abspath(os.path.join(api.image_folder, api.IMAGE_NAME)))

def parse_args():
    parser = argparse.ArgumentParser(description='ClientAPI Arguments')
    parser.add_argument('ip', type=str, help='IP address of server')
    parser.add_argument('timer', type=int, help='Time interval for API requests in seconds')
    parser.add_argument('--image_folder', type=str, default="wallpaper", help='Folder to save images')
    parser.add_argument('--save_as', type=str, default='image', help='Specify a custom image name prefix, example: "image"')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    api = client.ClientAPI(args.ip, args.timer, args.image_folder, args.save_as)
    mainloop(api)