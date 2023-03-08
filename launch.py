import time
import os

from src import client
from src import wallpaper

def mainloop():
    api = client.ClientAPI("http://127.0.0.1:5000/json", 5, "wallpaper")
    # json should look like this:
    # 	{"url": "http://127.0.0.1:5000/static/logo.png"}

    while True:
        time.sleep(api.SLEEP_TIME)
        api.delete_image()
        api.download_image()
        wallpaper.Wallpaper.set_wallpaper(os.path.abspath(os.path.join(api.image_folder, api.IMAGE_NAME)))

if __name__ == "__main__":
    mainloop()