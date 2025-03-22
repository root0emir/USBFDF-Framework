import unittest
from signature import identify_file_signature

class TestIdentifyFileSignature(unittest.TestCase):
    def setUp(self):
        self.test_files = {
            "example.jpg": "JPEG image",
            "example.png": "PNG image",
            "example.pdf": "PDF document",
            "example.gif": "GIF image",
            "example.bmp": "BMP image",
            "example.tiff": "TIFF image",
            "example.exe": "Windows executable",
            "example.zip": "ZIP archive",
            "example.rar": "RAR archive",
            "example.elf": "ELF executable",
            "example.ico": "ICO image",
            "example.gz": "GZIP archive",
            "example.bz2": "BZIP2 archive",
            "example.avi": "AVI video",
            "example.ttf": "TrueType font",
            "example.mp3": "MP3 audio",
            "example.wma": "Windows Media file",
            "example.flac": "FLAC audio",
            "example.ogg": "OGG audio",
            "example.mp4": "MP4 video",
            "example.mov": "QuickTime video",
            "example.mkv": "Matroska video",
            "example.doc": "Microsoft Office document",
            "example.docx": "Microsoft Office Open XML document",
            "example.ppt": "Microsoft Office document",
            "example.pptx": "Microsoft Office Open XML document",
            "example.xls": "Microsoft Office document",
            "example.xlsx": "Microsoft Office Open XML document",
        }

    def test_identify_file_signature(self):
        for file_path, expected_type in self.test_files.items():
            with self.subTest(file_path=file_path):
                self.assertEqual(identify_file_signature(file_path), expected_type)

if __name__ == "__main__":
    unittest.main()