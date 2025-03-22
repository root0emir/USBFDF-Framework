import os
import platform
import subprocess
import json
from device_detection import get_usb_devices
from file_analysis import analyze_device, analyze_file
from file_recovery import find_deleted_files
from logging_reporting import generate_report, log_analysis
from utils import install_requirements, get_device_info
from metadata_analysis import extract_exif_data, extract_mediainfo_data, extract_ffprobe_data
from hashing import calculate_hash, get_supported_algorithms
from file_signature import identify_file_signature

def print_ascii_art():
    art = """

          @@@@@@@@@@@@@@@@          
          @@@          @@@          
          @@@ @@@  @@@ @@@          
          @@@ @@@  @@@ @@@          
          @@@          @@@          
          @@@          @@@          
        @@@@@@@@@@@@@@@@@@@@            
       @@@@              @@@@       
       @@                  @@       
       @@                  @@       
       @@                  @@       
       @@                  @@       
       @@                  @@       
       @@                  @@       
       @@                  @@       
       @@                  @@       
       @@                  @@       
       @@@@              @@@@       
        @@@@@@@@@@@@@@@@@@@@        


 _   _ ____  ____  _____ ____  _____                          
| | | / ___|| __ )|  ___|  _ \|  ___|                         
| | | \___ \|  _ \| |_  | | | | |_                            
| |_| |___) | |_) |  _| | |_| |  _|                           
 \___/|____/|____/|_| __|____/|_|___        _____  ____  _  __
|  ___|  _ \    / \  |  \/  | ____\ \      / / _ \|  _ \| |/ /
| |_  | |_) |  / _ \ | |\/| |  _|  \ \ /\ / / | | | |_) | ' / 
|  _| |  _ <  / ___ \| |  | | |___  \ V  V /| |_| |  _ <| . \ 
|_|   |_| \_\/_/   \_\_|  |_|_____|  \_/\_/  \___/|_| \_\_|\_\                                                                  
                                                                    
    """
    print(art)

def print_menu():
    print("[ USBFDF-Framework / Developed by root0emir]")
    print("!-If you find any errors, please contact me.")
    print("-----USB Flash Drive Forensics Framework------")
    print("1. List all connected USB devices")
    print("2. Analyze a specified USB device")
    print("3. Analyze a specific file on the USB device")
    print("4. Recover deleted files from the specified USB device")
    print("5. Generate a report for the specified USB device")
    print("6. Log the analysis to a specified file")
    print("7. Extract EXIF metadata from a file")
    print("8. Extract MediaInfo metadata from a file")
    print("9. Extract FFprobe metadata from a file")
    print("10. Get detailed device information")
    print("11. Compute file hash")
    print("12. Identify file type by signature")
    print("--------------------------")
    print("13. Check required dependencies")
    print("14. Update the framework")
    print("15. Exit")

def update_framework():
    repo_url = "https://github.com/root0emir/USBFDF-Framework.git"
    temp_dir = "framework_update_temp"
    
    
    commands_windows = [
        f"git clone {repo_url} {temp_dir}",
        f"cd {temp_dir} && git pull",
        f"xcopy /E /Y {temp_dir}\\* .",
        f"rmdir /S /Q {temp_dir}"
    ]
    

    commands_unix = [
        f"git clone {repo_url} {temp_dir}",
        f"cd {temp_dir} && git pull",
        f"cp -r {temp_dir}/* .",
        f"rm -rf {temp_dir}"
    ]

    try:
 
        commands = commands_windows if platform.system() == 'Windows' else commands_unix
        
   
        for command in commands:
            subprocess.run(command, shell=True, check=True)
        
        print("Framework updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating the framework: {e}")
def main():
    print_ascii_art()
    
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            devices = get_usb_devices()
            print("Connected USB Devices:")
            for device in devices:
                print(f"- {device}")
        elif choice == '2':
            device_path = input("Enter the path to the USB device: ").strip()
            analysis_data = analyze_device(device_path)
            print(analysis_data)
        elif choice == '3':
            file_path = input("Enter the path to the file on the USB device: ").strip()
            analysis_data = analyze_file(file_path)
            print(analysis_data)
        elif choice == '4':
            device_path = input("Enter the path to the USB device: ").strip()
            deleted_files = find_deleted_files(device_path)
            print("Deleted Files:")
            for file in deleted_files:
                print(f"- {file}")
        elif choice == '5':
            device_path = input("Enter the path to the USB device: ").strip()
            analysis_data = analyze_device(device_path)
            report_path = os.path.join(device_path, 'analysis_report.txt')
            generate_report(analysis_data, report_path)
            print(f"Report generated at: {report_path}")
        elif choice == '6':
            log_file = input("Enter the path to the log file: ").strip()
            device_path = os.path.split(log_file)[0]
            analysis_data = analyze_device(device_path)
            log_analysis(log_file, analysis_data)
            print(f"Analysis logged at: {log_file}")
        elif choice == '7':
            file_path = input("Enter the path to the file: ").strip()
            exif_data = extract_exif_data(file_path)
            print(json.dumps(exif_data, indent=4))
        elif choice == '8':
            file_path = input("Enter the path to the file: ").strip()
            mediainfo_data = extract_mediainfo_data(file_path)
            print(json.dumps(mediainfo_data, indent=4))
        elif choice == '9':
            file_path = input("Enter the path to the file: ").strip()
            ffprobe_data = extract_ffprobe_data(file_path)
            print(json.dumps(ffprobe_data, indent=4))
        elif choice == '10':
            path = input("Enter the path to check: ").strip()
            device_info = get_device_info(path)
            print(json.dumps(device_info, indent=4))
        elif choice == '11':
            file_path = input("Enter the path to the file: ").strip()
            hash_type = input(f"Enter the hash type {get_supported_algorithms()}: ").strip()
            if hash_type in get_supported_algorithms():
                hash_value, file_size = calculate_hash(file_path, hash_type)
                print(f"Hash ({hash_type}): {hash_value}")
                print(f"File Size: {file_size} bytes")
            else:
                print(f"Unsupported hash type. Supported types are: {get_supported_algorithms()}")
        elif choice == '12':
            file_path = input("Enter the path to the file: ").strip()
            file_signature = identify_file_signature(file_path)
            print(f"The file signature is: {file_signature}")
        elif choice == '13':
            install_requirements()
        elif choice == '14':
            update_framework()
        elif choice == '15':
            print("Exiting... ")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 15.")

if __name__ == "__main__":
    main()
