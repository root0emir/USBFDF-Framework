import os
import argparse
import tsk
import datetime
from .recovery_helpers import open_image, save_recovered_file, log_event, backup_file

def find_deleted_files(device_path):
    deleted_files = []

    try:
        img_info = open_image(device_path)
        fs_info = tsk.FS_Info(img_info)
        root_dir = fs_info.open_dir(path="/")
        total_files = sum([len(files) for r, d, files in os.walk(device_path)])
        processed_files = 0

        for entry in root_dir:
            if entry.info.meta and entry.info.meta.type == tsk.TSK_FS_META_TYPE_REG and entry.info.meta.flags & tsk.TSK_FS_META_FLAG_UNALLOC:
                file_info = {
                    'name': entry.info.name.name.decode('utf-8'),
                    'size': entry.info.meta.size,
                    'creation_time': datetime.datetime.fromtimestamp(entry.info.meta.crtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'modification_time': datetime.datetime.fromtimestamp(entry.info.meta.mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'access_time': datetime.datetime.fromtimestamp(entry.info.meta.atime).strftime('%Y-%m-%d %H:%M:%S'),
                    'deletion_time': datetime.datetime.fromtimestamp(entry.info.meta.dtime).strftime('%Y-%m-%d %H:%M:%S')
                }

                try:
                    file_content = entry.read_random(0, entry.info.meta.size)
                    recovered_file_path = save_recovered_file(entry.info.name.name.decode('utf-8'), file_content)
                    backup_file(recovered_file_path)
                    file_info['recovered_path'] = recovered_file_path
                    log_event(f"File recovered: {recovered_file_path}")
                except Exception as e:
                    file_info['recovery_error'] = str(e)
                    log_event(f"Error recovering file {entry.info.name.name.decode('utf-8')}: {str(e)}")

                deleted_files.append(file_info)
                processed_files += 1
                print(f"Progress: {processed_files}/{total_files} files processed", end='\r')

    except Exception as e:
        log_event(f"Error: {e}")
        print(f"Error: {e}")

    return deleted_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recover deleted files from a disk image.")
    parser.add_argument("device_path", help="The path to the disk image file.")
    args = parser.parse_args()

    deleted_files = find_deleted_files(args.device_path)
    if deleted_files:
        print("Deleted Files:")
        for file in deleted_files:
            print(file)
    else:
        print("No deleted files found.")