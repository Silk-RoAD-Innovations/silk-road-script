import subprocess
import sys
import os

from typing_extensions import Literal

class NuitkaCompiler:
    def __init__(self, target_platform: Literal["windows", "macos", "linux"], main_script: str, icon: str = None) -> None:
        self.target_platform = target_platform.lower()
        self.main_script = main_script

        self.icon = icon

        if target_platform == "windows":
            self.requirements = "requirements-windows.txt"
            self.output_filename = f"app.exe"
        else:
            self.requirements = "requirements.txt"
            self.output_filename = "app"

        self.venv_name = os.path.abspath(f"venv_{self.target_platform}")
        self.executable = sys.executable

    def __create_venv(self):
        subprocess.run([self.executable, "-m", "venv", self.venv_name])

    def __change_executable_to_venv(self):
        if self.target_platform == "windows":
            self.executable = os.path.join(self.venv_name, "Scripts", "python.exe")
        else:
            self.executable = os.path.join(self.venv_name, "bin", "python")

    def __install_nuitka(self):
        # Updating pip
        subprocess.run([self.executable, "-m", "pip", "install", "--upgrade", "pip"])
        # Install nuitka for compilation
        subprocess.run([self.executable, "-m", "pip", "install", "nuitka"])

        # Install ordered-set for best Python compile time performance.
        subprocess.run([self.executable, "-m", "pip", "install", "ordered-set"])

        # Install 'zstandard' module for Nuitka-Onefile mode to compress.
        subprocess.run([self.executable, "-m", "pip", "install", "zstandard"])

    def __install_requirements(self):
        subprocess.run([self.executable, "-m", "pip", "install", "-r", self.requirements])

    def compile(self):
        '''Compile script to program'''
        self.__create_venv()
        self.__change_executable_to_venv()
        self.__install_nuitka()
        self.__install_requirements()

        if self.target_platform == "windows" and self.icon:
            subprocess.run(
                [self.executable, "-m", "nuitka", 
                "--follow-imports",
                "--onefile",
                f"--output-file={self.output_filename}",
                f"--windows-icon-from-ico={os.path.abspath(self.icon)}",
                "--output-dir=dist",
                self.main_script])
        else:
            subprocess.run(
                [self.executable, "-m", "nuitka", 
                "--follow-imports",
                "--onefile",
                f"--output-file={self.output_filename}",
                "--output-dir=dist",
                self.main_script])
if __name__ == "__main__":
    c = NuitkaCompiler("windows", "launch.py", "logo.ico")
    c.compile()