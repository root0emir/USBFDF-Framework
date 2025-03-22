from .signature_helper import load_known_signatures, read_file_header

def identify_file_signature(file_path):
    known_signatures = load_known_signatures()
    try:
        file_header = read_file_header(file_path, max_length=16)  # En uzun imzayı kapsayacak şekilde 16 bayt oku
        for signature, file_type in known_signatures.items():
            if file_header.startswith(signature):
                return file_type
        return 'Unknown file type'
    except Exception as e:
        return f"Error identifying file signature: {e}"

if __name__ == "__main__":
    test_files = [
        "example.jpg",
        "example.png",
        "example.pdf",
        "example.gif",
        "example.bmp",
        "example.tiff",
        "example.exe",
        "example.zip",
        "example.rar",
        "example.elf",
        "example.ico",
        "example.gz",
        "example.bz2",
        "example.avi",
        "example.ttf",
        "example.mp3",
        "example.wma",
        "example.flac",
        "example.ogg",
        "example.mp4",
        "example.mov",
        "example.mkv",
        "example.doc",
        "example.docx",
        "example.ppt",
        "example.pptx",
        "example.xls",
        "example.xlsx",
    ]
    for file in test_files:
        print(f"{file}: {identify_file_signature(file)}")