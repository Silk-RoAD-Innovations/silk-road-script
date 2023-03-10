# compile for macOS
python -m nuitka --standalone --plugin-enable=qt-plugins --plugin-enable=sqlite-extensions --output-dir=dist/macos --follow-imports launch.py

# compile for Linux
python -m nuitka --standalone --output-dir=dist/linux --follow-imports launch.py

# compile for Windows
python -m nuitka --standalone --output-dir=dist/windows --follow-imports --windows-icon-from-ico logo.ico launch.py