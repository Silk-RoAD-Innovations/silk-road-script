import os
import sys

if sys.platform == "win32":
    import winreg

class AutoLoad:
    def __init__(self, app_name):
        self.app_name = app_name

    def add_to_startup(self, file_path, args=''):
        if sys.platform == 'win32':
            # Add to Windows registry
            key = winreg.HKEY_CURRENT_USER
            key_value = "Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, key_value, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, self.app_name, 0, winreg.REG_SZ, f'"{file_path}" {args}')
        elif sys.platform == 'darwin':
            # Add to macOS launch agents
            plist_path = os.path.expanduser(f'~/Library/LaunchAgents/com.{self.app_name}.plist')
            with open(plist_path, 'w') as plist:
                plist.write(f'''<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
                "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
                <plist version="1.0">
                <dict>
                    <key>Label</key>
                    <string>com.{self.app_name}</string>
                    <key>ProgramArguments</key>
                    <array>
                        <string>{file_path}</string>
                        <string>{args}</string>
                    </array>
                    <key>RunAtLoad</key>
                    <true/>
                </dict>
                </plist>''')
        elif sys.platform.startswith('linux'):
            # Add to Linux autostart folder
            autostart_dir = os.path.expanduser('~/.config/autostart')
            os.makedirs(autostart_dir, exist_ok=True)
            desktop_file_path = os.path.join(autostart_dir, f'{self.app_name}.desktop')
            with open(desktop_file_path, 'w') as desktop_file:
                desktop_file.write(f'''[Desktop Entry]
                Type=Application
                Exec={file_path} {args}
                Hidden=false
                NoDisplay=false
                X-GNOME-Autostart-enabled=true
                Name[en_US]={self.app_name}
                Name={self.app_name}
                Comment[en_US]={self.app_name} startup script
                Comment={self.app_name} startup script''')

    def remove_from_startup(self):
        if sys.platform == 'win32':
            # Remove from Windows registry
            key = winreg.HKEY_CURRENT_USER
            key_value = "Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, key_value, 0, winreg.KEY_WRITE) as key:
                winreg.DeleteValue(key, self.app_name)
        elif sys.platform == 'darwin':
            # Remove from macOS launch agents
            plist_path = os.path.expanduser(f'~/Library/LaunchAgents/com.{self.app_name}.plist')
            if os.path.exists(plist_path):
                os.remove(plist_path)
        elif sys.platform.startswith('linux'):
            # Remove from Linux autostart folder
            desktop_file_path = os.path.expanduser(f'~/.config/autostart/{self.app_name}.desktop')
            if os.path.exists(desktop_file_path):
                os.remove(desktop_file_path)