import os
import tsk

def open_image(image_path):
    return tsk.Img_Info(image_path)

def save_recovered_file(file_name, file_content):
    recovered_path = os.path.join('recovered_files', file_name)
    os.makedirs(os.path.dirname(recovered_path), exist_ok=True)
    with open(recovered_path, 'wb') as recovered_file:
        recovered_file.write(file_content)
    return recovered_path

def log_event(message):
    with open('recovery.log', 'a') as log_file:
        log_file.write(message + '\n')

def backup_file(file_path):
    backup_path = file_path + '.bak'
    with open(file_path, 'rb') as original_file:
        with open(backup_path, 'wb') as backup_file:
            backup_file.write(original_file.read())