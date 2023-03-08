import os
import imghdr
import requests

class ClientAPI:
	def __init__(self, ip: str, timer: int, image_folder: str = "image_folder", save_as: str = "image") -> None:
		'''Class for interacting with main server'''
		self.HOST = ip
		self.SLEEP_TIME = timer # Sets how often will client try to access server

		self.image_folder = image_folder
		self.save_as = save_as
		if not os.path.exists(self.image_folder):
			os.mkdir(self.image_folder)
		try:
			self.IMAGE_NAME = os.listdir(self.IMAGE_NAME)[0]
		except:
			self.IMAGE_NAME = ""

	def delete_image(self):
		'''Deleting previous image in image_folder'''
		try:
			os.remove(os.path.join(self.image_folder, os.listdir(self.image_folder)[0]))
		
		# If image doesn't exists
		except IndexError:
			pass

	def __save_image(self, response):
		'''Creating image file'''
		with open(os.path.join(self.image_folder, self.IMAGE_NAME), "wb") as file:
				file.write(response.content)

	def download_image(self):
		try:
			# Getting json that contains url to image
			response = requests.get(self.HOST)
			image_url = response.json()["url"]

			# Downloading image from json's url
			response = requests.get(image_url)

			# Getting the file type of the image using imghdr
			file_type = imghdr.what(None, response.content)
			self.IMAGE_NAME = f"{self.save_as}.{file_type}"
			self.__save_image(response)

		except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
			# Retries to connect to the api, if it couldn't
			self.download_image()