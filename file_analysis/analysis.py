import os
import time
import json
import platform
import stat
import magic 
from hashlib import md5, sha1
from file_signature.signature import identify_file_signature
from metadata_analysis.metadata import extract_exif_data

def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.{decimal_places}f} {unit}"
        size /= 1024

def human_readable_permissions(mode):
    is_dir = 'd' if stat.S_ISDIR(mode) else '-'
    dic = {
        '7': 'rwx', '6': 'rw-', '5': 'r-x', '4': 'r--',
        '3': '-wx', '2': '-w-', '1': '--x', '0': '---',
    }
    perm = str(oct(mode)[-3:])
    human_perm = ''.join(dic.get(x, x) for x in perm)
    return is_dir + human_perm

def calculate_md5(file_path):
    hash_md5 = md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def calculate_sha1(file_path):
    hash_sha1 = sha1()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()

def analyze_device(device_path, output_format='json'):
    analysis_data = []
    for root, dirs, files in os.walk(device_path):
        for file in files:
            file_path = os.path.join(root, file)
            analysis_data.append(analyze_file(file_path))

    if output_format == 'json':
        return json.dumps(analysis_data, indent=2)
    elif output_format == 'text':
        return "\n".join([json.dumps(data, indent=2) for data in analysis_data])
    else:
        return "Unsupported output format. Please choose 'json' or 'text'."

def analyze_file(file_path):
    try:
        file_stat = os.stat(file_path)
        file_info = {
            "file_path": file_path,
            "size": human_readable_size(file_stat.st_size),
            "created": time.ctime(file_stat.st_ctime),
            "modified": time.ctime(file_stat.st_mtime),
            "accessed": time.ctime(file_stat.st_atime),
            "md5": calculate_md5(file_path),
            "sha1": calculate_sha1(file_path),
            "file_type": magic.from_file(file_path, mime=True),
            "file_signature": identify_file_signature(file_path),
            "exif_data": extract_exif_data(file_path),
            "permissions": human_readable_permissions(file_stat.st_mode),
            "inode": file_stat.st_ino
        }

        # Platforma bağlı olarak kullanıcı ve grup bilgilerini ekle
        if platform.system() != 'Windows':
            import pwd
            import grp
            file_info["owner"] = pwd.getpwuid(file_stat.st_uid).pw_name
            file_info["group"] = grp.getgrgid(file_stat.st_gid).gr_name
        else:
            file_info["owner"] = os.getlogin()
            file_info["group"] = os.environ.get('USERDOMAIN', 'Unknown')

        return file_info
    except Exception as e:
        return {"error": str(e), "file_path": file_path}

if __name__ == "__main__":
    device_path = input("Enter the path to the USB device: ").strip()
    output_format = input("Enter output format (json/text): ").strip().lower()
    analysis_results = analyze_device(device_path, output_format)
    print(analysis_results)