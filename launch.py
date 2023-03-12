import time
import os
import sys
from datetime import datetime, timezone, timedelta

import argparse
import requests

from src import client
from scripts import wallpaper
from scripts import autoload

__version__ = 0

def mainloop(api: client.ClientAPI):
    '''Function to call to ClientAPI every X seconds, and set downloaded image as wallpaper'''
    gmt = timezone(timedelta(hours=6)) # GMT+6
    def download_image_retry():
        '''Retries to connect to the api after SLEEP_TIME, if it couldn't'''
        try:
            api.download_image()
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            time.sleep(api.SLEEP_TIME)
            download_image_retry()

    while True:
        now = datetime.now(gmt)
        next_time = now.replace(minute=(now.minute // api.SLEEP_TIME + 1) * api.SLEEP_TIME, second=0, microsecond=0)
        wait_time = (next_time - now).total_seconds()
        api.delete_image()
        download_image_retry()
        wallpaper.Wallpaper.set_wallpaper(os.path.abspath(os.path.join(api.image_folder, api.IMAGE_NAME)))
        time.sleep(wait_time)

def parse_args():
    parser = argparse.ArgumentParser(description='ClientAPI Arguments')
    parser.add_argument('ip', type=str, help='IP address of server')
    parser.add_argument('timer', type=int, help='Time interval for API requests in minutes')
    parser.add_argument('--image_folder', type=str, default=os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "wallpaper"), help='Folder to save images')
    parser.add_argument('--save_as', type=str, default="image", help='Specify a custom image name prefix, example: "image"')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    exe_path = os.path.abspath(sys.argv[0])
    args = parse_args()
    a = autoload.AutoLoad("wallpaper_changer")
    a.add_to_startup(exe_path, f"{args.ip} {args.timer} --image_folder {args.image_folder} --save_as {args.save_as}")
    api = client.ClientAPI(args.ip, args.timer, args.image_folder, args.save_as)
    mainloop(api)