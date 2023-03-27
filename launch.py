import time
import os
import sys
from datetime import datetime, timezone, timedelta
import subprocess
from urllib.parse import urlparse

import argparse
import requests

from src import client
from scripts import wallpaper
from scripts import autoload

__version__ = 0

class Scheduler:
	def __init__(self, api: client.ClientAPI) -> None:
		self.api = api

	def image_mainloop(self, interval: int):
		'''Function to call to ClientAPI every X seconds, and set downloaded image as wallpaper'''
		gmt = timezone(timedelta(hours=6)) # GMT+6
		def download_image_retry():
			'''Retries to connect to the api after SLEEP_TIME, if it couldn't'''
			try:
				self.api.download_image()
			except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
				time.sleep(interval)
				download_image_retry()

		while True:
			now = datetime.now(gmt)
			next_time = now.replace(minute=(now.minute // interval + 1) * interval, second=0, microsecond=0)
			wait_time = (next_time - now).total_seconds()
			self.api.delete_image()
			download_image_retry()
			wallpaper.Wallpaper.set_wallpaper(os.path.abspath(os.path.join(self.api.image_folder, self.api.IMAGE_NAME)))
			time.sleep(wait_time)


	def update_mainloop(self):
		#TODO finish the function
		while True:
			now = datetime.now()

			# Calculate the number of seconds until 0:00
			midnight = datetime(now.year, now.month, now.day, 0, 0)
			seconds_until_midnight = (midnight - now).seconds

			update_info = self.api.check_for_updates()

			if update_info["version"] > __version__:
				def download_and_run(url: str, name: str):
					# Download the executable from the given URL
					response = requests.get(url)
					exe_file = name
					if os.path.exists(name):
						pass

					with open(exe_file, 'wb') as f:
						f.write(response.content)
					
					# Run the executable
					subprocess.call(exe_file)

					# Remove this file
					os.remove(os.path.abspath(sys.argv[0]))

			time.sleep(seconds_until_midnight)


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
    parsed_ip = urlparse(args.ip)
    try:
        ip_address = parsed_ip.scheme + "://" + parsed_ip.hostname + ':' + str(parsed_ip.port)
    except AttributeError:
        ip_address = parsed_ip.scheme + "://" + parsed_ip.hostname

    print(ip_address)

    # a = autoload.AutoLoad("wallpaper_changer")
    # a.add_to_startup(exe_path, f"{args.ip} {args.timer} --image_folder {args.image_folder} --save_as {args.save_as}")
    # api = client.ClientAPI(args.ip, args.timer, args.image_folder, args.save_as)
    # mainloop(api)