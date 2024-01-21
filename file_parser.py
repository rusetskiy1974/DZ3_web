from pathlib import Path
from threading import Thread


IMAGES = []
VIDEO = []
DOCUMENTS = []
AUDIO = []
OTHER = []
ARCHIVES = []
FOLDERS = []

EXTENSIONS = set()
UNKNOWN = set()

REGISTER_EXTENSIONS = {
    'JPEG': IMAGES,
    'PNG': IMAGES,
    'JPG': IMAGES,
    'SVG': IMAGES,
    'AVI': VIDEO,
    'MP4': VIDEO,
    'MOV': VIDEO,
    'MKV': VIDEO,
    'DOC': DOCUMENTS,
    'DOCX': DOCUMENTS,
    'TXT': DOCUMENTS,
    'PDF': DOCUMENTS,
    'XLSX': DOCUMENTS,
    'PPTX': DOCUMENTS,
    'MP3': AUDIO,
    'OGG': AUDIO,
    'WAV': AUDIO,
    'AMR': AUDIO,
    'GZ': ARCHIVES,
    'TAR': ARCHIVES,
    'ZIP': ARCHIVES,
}


def get_extension(file_name: str) -> str:
    return Path(file_name).suffix[1:].upper()


def scan(folder: Path) -> None:
    threads = []

    def scan_folders(folder_):
        for item in folder_.iterdir():
            if item.is_dir():
                if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'OTHER'):
                    FOLDERS.append(item)
                    if item.parent == folder:
                        thread = Thread(target=scan_folders, args=(item, ))
                        threads.append(thread)
                        thread.start()
                        continue
                    scan_folders(item)
                continue
            ext = get_extension(item.name)
            full_name = folder_ / item.name
            if not ext:
                OTHER.append(full_name)
            else:
                try:
                    container = REGISTER_EXTENSIONS[ext]
                    EXTENSIONS.add(ext)
                    container.append(full_name)
                except KeyError:
                    UNKNOWN.add(ext)
                    OTHER.append(full_name)
    scan_folders(folder)

    for th in threads:
        th.join()

