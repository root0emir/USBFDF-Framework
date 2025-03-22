import os
import platform
import subprocess
import json

def get_usb_devices():
    devices = []
    system = platform.system()
    
    try:
        # Linux platformunda lsblk komutunu kullanarak USB cihazlarını tespit etme
        if system == 'Linux':
            lsblk_output = subprocess.check_output(['lsblk', '-J']).decode('utf-8')
            lsblk_data = json.loads(lsblk_output)

            for device in lsblk_data.get('blockdevices', []):
                if 'children' in device:
                    for child in device['children']:
                        mountpoint = child.get('mountpoint')
                        if mountpoint and mountpoint.startswith('/media'):
                            device_info = {
                                'name': child.get('name'),
                                'mountpoint': mountpoint,
                                'size': child.get('size'),
                                'type': child.get('type'),
                                'fstype': child.get('fstype'),
                                'model': device.get('model'),
                                'serial': device.get('serial')
                            }
                            devices.append(device_info)
        # Windows platformunda wmic komutunu kullanarak USB cihazlarını tespit etme
        elif system == 'Windows':
            wmic_output = subprocess.check_output(['wmic', 'logicaldisk', 'get', 'name,description,filesystem,size']).decode('utf-8')
            lines = wmic_output.strip().split('\n')
            for line in lines[1:]:
                parts = line.split()
                if 'Removable' in parts[0]:
                    device_info = {
                        'name': parts[1],
                        'filesystem': parts[2],
                        'size': parts[3]
                    }
                    devices.append(device_info)
        else:
            print(f"Unsupported platform: {system}")

    except subprocess.CalledProcessError as e:
        print(f"Failed to get USB devices: {e}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse lsblk output: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return devices

if __name__ == "__main__":
    usb_devices = get_usb_devices()
    if usb_devices:
        print("Detected USB Devices:")
        for device in usb_devices:
            print(json.dumps(device, indent=2))
    else:
        print("No USB devices found.")