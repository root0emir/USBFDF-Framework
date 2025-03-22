def load_known_signatures():
    return {
        b'\xFF\xD8\xFF': 'JPEG image',
        b'\x89\x50\x4E\x47': 'PNG image',
        b'\x25\x50\x44\x46': 'PDF document',
        b'\x47\x49\x46\x38': 'GIF image',
        b'\x42\x4D': 'BMP image',
        b'\x49\x49\x2A\x00': 'TIFF image',
        b'\x4D\x5A': 'Windows executable',
        b'\x50\x4B\x03\x04': 'ZIP archive',
        b'\x52\x61\x72\x21': 'RAR archive',
        b'\x7F\x45\x4C\x46': 'ELF executable',
        b'\x00\x00\x01\x00': 'ICO image',
        b'\x1F\x8B\x08': 'GZIP archive',
        b'\x42\x5A\x68': 'BZIP2 archive',
        b'\x52\x49\x46\x46': 'AVI video',
        b'\x00\x01\x00\x00': 'TrueType font',
        b'\xFF\xFB': 'MP3 audio',
        b'\x49\x44\x33': 'MP3 audio',
        b'\x30\x26\xB2\x75': 'Windows Media file',
        b'\x66\x4C\x61\x43': 'FLAC audio',
        b'\x4F\x67\x67\x53': 'OGG audio',
        b'\x00\x00\x00\x18\x66\x74\x79\x70\x33\x67\x70\x35': 'MP4 video',
        b'\x00\x00\x00\x14\x66\x74\x79\x70\x71\x74\x20\x20': 'QuickTime video',
        b'\x1A\x45\xDF\xA3': 'Matroska video',
        b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1': 'Microsoft Office document',
        b'\x50\x4B\x03\x04\x14\x00\x06\x00': 'Microsoft Office Open XML document',
        # Diğer bilinen dosya imzaları eklenebilir
    }

def read_file_header(file_path, max_length=16):
    with open(file_path, 'rb') as f:
        return f.read(max_length)