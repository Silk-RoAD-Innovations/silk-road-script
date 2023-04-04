import time
import os
import sys
import subprocess
import logging
from datetime import datetime, timezone, timedelta
from threading import Thread

import argparse
import requests

from src import client
from scripts import wallpaper
from scripts import autoload

__version__ = 0

# Creating logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

class Scheduler:
	def __init__(self, api: client.ClientAPI, interval) -> None:
		self.api = api
		self.interval = interval

	def image_mainloop(self):
		'''Function to call to ClientAPI every X seconds, and set downloaded image as wallpaper'''
		gmt = timezone(timedelta(hours=6)) # GMT+6

		logger.info("Starting image mainloop.")
		while True:
			now = datetime.now(gmt)
			next_time = now.replace(minute=(now.minute // self.interval + 1) * self.interval, second=0, microsecond=0)
			wait_time = (next_time - now).total_seconds()

			self.api.delete_image()
			try:
				logger.info("Trying to download image.")
				self.api.download_image()
			except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError, requests.exceptions.JSONDecodeError):
				logger.error(f"The json for images doesn't exist at {self.api.HOST}")
			else:
				logger.info("The image was successfully downloaded, setting it as a wallpaper.")
				wallpaper.Wallpaper.set_wallpaper(os.path.abspath(os.path.join(self.api.image_folder, self.api.IMAGE_NAME)))
			logger.info(f"Next check for image in: {wait_time} seconds")
			time.sleep(wait_time)

	def update_mainloop(self):
		'''Function to call to ClientAPI everyday at 0:00, and check for updates'''
		def download_and_run(url: str, name: str):
			# Download the executable from the given URL
			response = requests.get(url)
			if response.status_code == 404:
				return
			exe_file = name
			if os.path.exists(name):
				pass

			with open(exe_file, 'wb') as f:
				f.write(response.content)

			# Run the executable with arguments
			subprocess.call(exe_file, self.api.HOST, self.interval, self.api.image_folder, self.api.save_as)

			# Remove this file
			os.remove(os.path.abspath(sys.argv[0]))

		logger.info("Starting update mainloop.")
		while True:
			now = datetime.now()

			# Calculate the number of seconds until 0:00
			midnight = datetime(now.year, now.month, now.day, 0, 0)
			seconds_until_midnight = (midnight - now).seconds
			

			logger.info("Trying to check for updates.")
			try:
				update_info = self.api.check_for_updates()

			except requests.exceptions.JSONDecodeError:
				logger.error(f"The json for updates doesn't exist at '{self.api.get_url()}/wallpaper/update', please check if your IP is correct.")

			else:
				if update_info["version"] > __version__:
					logger.info("New update was found, installing.")
					download_and_run(update_info["update"], f"wallpaper_core_{update_info['version']}.exe")


			logger.info(f"Next check for update in: {seconds_until_midnight} seconds")
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
	logger.info("Launching program.")

	logger.info("Adding program to the autoload.")
	# a = autoload.AutoLoad("wallpaper_changer")
	# a.add_to_startup(exe_path, f"{args.ip} {args.timer} --image_folder {args.image_folder} --save_as {args.save_as}")

	api = client.ClientAPI(args.ip, args.image_folder, args.save_as)
	scheduler = Scheduler(api, 1)
	t1 = Thread(target=scheduler.image_mainloop)
	t2 = Thread(target=scheduler.update_mainloop)
	t1.start()
	t2.start()