import os
import sys
import imghdr
import requests
from urllib.parse import urlparse

from typing import Dict

class ClientAPI:
	'''Class for interacting with main server'''
	def __init__(self, ip: str,
	    		image_folder: str = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "wallpaper"),
				save_as: str = "image") -> None:
		self.HOST = ip

		self.image_folder = image_folder
		self.save_as = save_as
		if not os.path.exists(self.image_folder):
			os.mkdir(self.image_folder)
		try:
			self.IMAGE_NAME = os.listdir(self.IMAGE_NAME)[0]
		except:
			self.IMAGE_NAME = ""

	def delete_image(self) -> None:
		'''Deleting previous image in image_folder'''
		try:
			os.remove(os.path.join(self.image_folder, os.listdir(self.image_folder)[0]))
		
		# If image doesn't exists
		except (IndexError, FileNotFoundError):
			pass

	def __save_image(self, response: requests.Response) -> None:
		'''Creating image file'''
		if not os.path.exists(self.image_folder):
			os.mkdir(self.image_folder)
		with open(os.path.join(self.image_folder, self.IMAGE_NAME), "wb") as file:
			file.write(response.content)

	def download_image(self):
		'''Downloads an image from server'''
		# Getting json that contains url to image
		json_response = requests.get(self.HOST)
		image_url = json_response.json()["url"]

		# Downloading image from json's url
		response = requests.get(image_url)

		# Getting the file type of the image using imghdr
		file_type = imghdr.what(None, response.content)
		self.IMAGE_NAME = f"{self.save_as}.{file_type}"
		self.__save_image(response)

	def check_for_updates(self) -> Dict:
		parsed_ip = urlparse(self.HOST)
		try:
			if parsed_ip.port:
				ip_address = parsed_ip.scheme + "://" + parsed_ip.hostname + ':' + str(parsed_ip.port)
			else:
				ip_address = parsed_ip.scheme + "://" + parsed_ip.hostname
		except AttributeError:
			ip_address = parsed_ip.scheme + "://" + parsed_ip.hostname
		response = requests.get(f"{ip_address}/wallpaper/update").json()
		return response