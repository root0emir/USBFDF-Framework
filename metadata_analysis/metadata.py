import subprocess
import json
import argparse
import shutil
import platform

def check_tool(tool_name):
    """Check if a tool is installed."""
    return shutil.which(tool_name) is not None

def install_tool(tool_name):
    """Install a tool using the system package manager."""
    os_name = platform.system()
    try:
        if os_name == "Linux":
            subprocess.run(['sudo', 'apt-get', 'install', '-y', tool_name], check=True)
        elif os_name == "Windows":
            if tool_name == "exiftool":
                print("Please download and install ExifTool from: https://exiftool.org/")
            elif tool_name == "mediainfo":
                print("Please download and install MediaInfo from: https://mediaarea.net/en/MediaInfo/Download/Windows")
            elif tool_name == "ffprobe":
                print("Please download and install FFmpeg from: https://ffmpeg.org/download.html")
        print(f"{tool_name} installed successfully or follow the instructions to install.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {tool_name}: {e}")

def extract_exif_data(file_path):
    """Extract EXIF data using exiftool."""
    if not check_tool('exiftool'):
        return "ExifTool not found. Please install it to extract EXIF data."
    try:
        result = subprocess.run(['exiftool', '-json', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            return f"Error extracting EXIF data: {result.stderr.decode('utf-8')}"
        exif_data = result.stdout.decode('utf-8')
        return json.loads(exif_data)
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def extract_mediainfo_data(file_path):
    """Extract metadata using mediainfo."""
    if not check_tool('mediainfo'):
        return "MediaInfo not found. Please install it to extract metadata."
    try:
        result = subprocess.run(['mediainfo', '--Output=JSON', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            return f"Error extracting MediaInfo data: {result.stderr.decode('utf-8')}"
        mediainfo_data = result.stdout.decode('utf-8')
        return json.loads(mediainfo_data)
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def extract_ffprobe_data(file_path):
    """Extract metadata using ffprobe."""
    if not check_tool('ffprobe'):
        return "ffprobe not found. Please install it to extract metadata."
    try:
        result = subprocess.run(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            return f"Error extracting ffprobe data: {result.stderr.decode('utf-8')}"
        ffprobe_data = result.stdout.decode('utf-8')
        return json.loads(ffprobe_data)
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def main():
    parser = argparse.ArgumentParser(description="Extract metadata from a file using various tools.")
    parser.add_argument("file_path", help="The path to the file.")
    parser.add_argument("tool", choices=["exiftool", "mediainfo", "ffprobe"], help="The tool to use for extracting metadata.")
    parser.add_argument("--install", action="store_true", help="Install the selected tool if it is not already installed.")
    args = parser.parse_args()

    if args.install and not check_tool(args.tool):
        install_tool(args.tool)

    if args.tool == "exiftool":
        metadata = extract_exif_data(args.file_path)
    elif args.tool == "mediainfo":
        metadata = extract_mediainfo_data(args.file_path)
    elif args.tool == "ffprobe":
        metadata = extract_ffprobe_data(args.file_path)

    if isinstance(metadata, str):
        print(metadata)
    else:
        print(json.dumps(metadata, indent=4))

if __name__ == "__main__":
    main()