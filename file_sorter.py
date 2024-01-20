from pathlib import Path
import shutil

from normalize import normalize
import file_parser as parser
import concurrent.futures
from threading import Thread, RLock



class FileSorter:
    def __init__(self, folder):
        self.folder = folder

    def handle_media(self, filename: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / normalize(filename.name))

    def handle_other(self, filename: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / normalize(filename.name))

    def handle_archive(self, filename: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
        folder_for_file.mkdir(exist_ok=True, parents=True)
        try:
            shutil.unpack_archive(str(filename.resolve()), str(folder_for_file.resolve()))
        except shutil.ReadError:
            folder_for_file.rmdir()
            return None
        filename.unlink()

    def handle_folder(self, folder: Path):
        try:
            folder.rmdir()
        except OSError:
            print(f'Не вдалося видалити папку {folder.resolve()}')

    def func(self, value):
        exec(value)

    def sort_files(self):
        parser.scan(self.folder)

        container = (
            "for file in parser.IMAGES:\n self.handle_media(file, self.folder/'images')",
            "for file in parser.VIDEO:\n self.handle_media(file, self.folder/'video')",
            "for file in parser.AUDIO:\n self.handle_media(file, self.folder/'audio')",
            "for file in parser.DOCUMENTS:\n self.handle_media(file, self.folder/'documents')",
            "for file in parser.OTHER:\n self.handle_other(file, self.folder/'OTHER')",
            "for file in parser.ARCHIVES:\n self.handle_archive(file, self.folder/'archives')",
            "for folder_to_handle in parser.FOLDERS[::-1]:\n self.handle_folder(folder_to_handle)",
        )

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(self.func, container)


        #

        # for file in parser.IMAGES:
        #     self.handle_media(file, self.folder / 'images')
        #
        # for file in parser.VIDEO:
        #     self.handle_media(file, self.folder / 'video')
        #
        # for file in parser.AUDIO:
        #     self.handle_media(file, self.folder / 'audio')
        #
        # for file in parser.DOCUMENTS:
        #     self.handle_media(file, self.folder / 'documents')
        #
        # for file in parser.OTHER:
        #     self.handle_other(file, self.folder / 'OTHER')
        #
        # for file in parser.ARCHIVES:
        #     self.handle_archive(file, self.folder / 'archives')
        #
        # for folder_to_handle in parser.FOLDERS[::-1]:
        #     self.handle_folder(folder_to_handle)



