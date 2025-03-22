import os
import argparse
import platform
import json
import shutil
import subprocess
import sys


if platform.system() == "Windows":
    try:
        import win32api
        import win32netcon
        import win32wnet
    except ImportError:
        print("Loading modules...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pywin32'])
        import win32api
        import win32netcon
        import win32wnet

def is_usb_device(path):
    """Check if the given path is a USB device."""
    try:
        if os.path.exists(path) and ('/media' in path or '/mnt' in path):
            return True
        return False
    except Exception as e:
        print(f"Error checking if path is a USB device: {e}")
        return False

def is_cdrom_device(path):
    """Check if the given path is a CD-ROM device."""
    try:
        if os.path.exists(path) and 'cdrom' in path.lower():
            return True
        return False
    except Exception as e:
        print(f"Error checking if path is a CD-ROM device: {e}")
        return False

def is_network_drive(path):
    """Check if the given path is a network drive."""
    try:
        if platform.system() == "Windows":
            if win32wnet and win32netcon:
                drive_type = win32wnet.WNetGetUniversalName(path, win32netcon.REMOTE_NAME_INFO_LEVEL)
                if drive_type == win32netcon.RESOURCETYPE_DISK:
                    return True
        else:
            if os.path.ismount(path) and 'nfs' in os.popen(f'df -T {path}').read():
                return True
        return False
    except Exception as e:
        print(f"Error checking if path is a network drive: {e}")
        return False

def get_filesystem_type(path):
    """Get the filesystem type of the given path."""
    try:
        if platform.system() == "Windows":
            if win32api:
                return win32api.GetVolumeInformation(path)[4]
            else:
                return "Unknown"
        else:
            return os.popen(f'df -T {path}').read().split()[1]
    except Exception as e:
        print(f"Error getting filesystem type: {e}")
        return "Unknown"

def get_device_info(path):
    """Get device information."""
    try:
        if not os.path.exists(path):
            return f"Path {path} does not exist."
        device_info = {
            "path": path,
            "is_usb": is_usb_device(path),
            "is_cdrom": is_cdrom_device(path),
            "is_network_drive": is_network_drive(path),
            "size": os.path.getsize(path) if os.path.isfile(path) else "N/A",
            "total_size": shutil.disk_usage(path).total if os.path.exists(path) else "N/A",
            "free_space": shutil.disk_usage(path).free if os.path.exists(path) else "N/A",
            "filesystem": get_filesystem_type(path),
            "type": "File" if os.path.isfile(path) else "Directory" if os.path.isdir(path) else "Other"
        }
        return device_info
    except Exception as e:
        return f"Error getting device information: {e}"

def main():
    parser = argparse.ArgumentParser(description="Utility functions for device checks.")
    parser.add_argument("path", help="The path to check.")
    args = parser.parse_args()

    device_info = get_device_info(args.path)
    print(json.dumps(device_info))

if __name__ == "__main__":
    main()
