import sys
import os
import subprocess

if sys.platform == "win32":
	import win32api
	import win32con
	import win32gui

class Wallpaper:

	@staticmethod
	def set_wallpaper(path):
		if sys.platform == "win32":
			key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)

			win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "6")			
			win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
			win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path, win32con.SPIF_SENDWININICHANGE)
		elif "linux" in sys.platform:
			os.system(f"gsettings set org.gnome.desktop.background picture-uri file:{path}")
		elif "darwin" in sys.platform:
			SCRIPT = """/usr/bin/osascript<<END
						tell application "Finder"
						set desktop picture to POSIX file "%s"
						end tell
						END"""
			subprocess.Popen(SCRIPT%path, shell=True)

