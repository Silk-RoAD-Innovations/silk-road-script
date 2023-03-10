import os
import shutil
import sys

def compile_windows():
    # Get the absolute path to the icon file
    icon_path = os.path.abspath("logo.ico")

    # Create a new virtual environment
    env_dir = os.path.abspath("venv_windows")
    if os.path.exists(env_dir):
        shutil.rmtree(env_dir)
    os.system(f"{sys.executable} -m venv {env_dir}")

    # Activate the virtual environment and install dependencies
    activate_script = os.path.join(env_dir, "Scripts", "activate")
    os.system(f"cmd /c {activate_script} && pip install -r requirements-windows.txt -r requirements.txt")

    # Compile the code and create a single executable
    output_path = os.path.abspath("dist/windows/myapp.exe")
    command = f"python -m nuitka --standalone --output-file={output_path} --follow-imports --windows-icon-from-ico={icon_path} launch.py"
    os.system(command)

def compile_linux():
    # Create a new virtual environment
    env_dir = os.path.abspath("venv_linux")
    if os.path.exists(env_dir):
        shutil.rmtree(env_dir)
    os.system(f"{sys.executable} -m venv {env_dir}")

    # Activate the virtual environment and install dependencies
    activate_script = os.path.join(env_dir, "bin", "activate")
    os.system(f"source {activate_script} && pip install -r requirements.txt")

    # Compile the code and create a single executable
    output_path = os.path.abspath("dist/linux/myapp")
    command = f"python -m nuitka --standalone --output-file={output_path} --follow-imports launch.py"
    os.system(command)

def compile_mac_os():
    # Create a new virtual environment
    env_dir = os.path.abspath("venv_macos")
    if os.path.exists(env_dir):
        shutil.rmtree(env_dir)
    os.system(f"{sys.executable} -m venv {env_dir}")

    # Activate the virtual environment and install dependencies
    activate_script = os.path.join(env_dir, "bin", "activate")
    os.system(f"source {activate_script} && pip install -r requirements.txt")

    # Compile the code and create a single executable
    output_path = os.path.abspath("dist/macos/myapp")
    command = f"python -m nuitka --standalone --output-file={output_path} --plugin-enable=qt-plugins --plugin-enable=sqlite-extensions --follow-imports launch.py"
    os.system(command)

if __name__ == "__main__":
    if sys.platform == "win32":
        compile_windows()
    elif "darwin" in sys.platform:
        compile_mac_os()
    elif "linux" in sys.platform:
        compile_linux()
