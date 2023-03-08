import requests
import imghdr
import time
import os

from wallpaper import Wallpaper

class ClientAPI:
	def __init__(self, ip: str) -> None:
		self.HOST = ip
		self.SLEEP_TIME = 1

		self.WALLPAPER_PATH = "wallpaper"
		try:
			self.IMAGE_NAME = os.listdir(self.IMAGE_NAME)[0]
		except:
			self.IMAGE_NAME = ""


	def mainloop(self):
		while True:
			time.sleep(self.SLEEP_TIME)
			self.__delete_image()
			self.download_content()
			Wallpaper.set_wallpaper(os.path.abspath(os.path.join(self.WALLPAPER_PATH,self.IMAGE_NAME)))


	def __delete_image(self):
		'''Deleting previous image in wallpaper folder'''
		try:
			os.remove(os.path.join(self.WALLPAPER_PATH, os.listdir(self.WALLPAPER_PATH)[0]))
		except:
			pass

	def __write_to_file(self, file_type, response):
		'''Creating image file'''
		with open(os.path.join(self.WALLPAPER_PATH, f"1.{file_type}"), "wb") as file:
				file.write(response.content)


	def download_content(self):
		try:
			response = requests.get(self.HOST)
			# Get the file type of the image using imghdr
			file_type = imghdr.what(None, response.content)
			self.__write_to_file(file_type=file_type, response=response)
			self.IMAGE_NAME = f"1.{file_type}"

		except requests.exceptions.ConnectTimeout:
			# Retries to connect to the api, if couldn't
			self.download_content()