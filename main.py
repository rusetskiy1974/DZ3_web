from pathlib import Path
from file_sorter import FileSorter
from time import perf_counter


def start():
    try:
        folder_for_scan = input('Enter folder for scan: ')
        if folder_for_scan:
            start_time = perf_counter()
            sorter = FileSorter(Path(folder_for_scan))
            sorter.sort_files()
            end_time = perf_counter()
            print(f'Work time {end_time - start_time: 0.2f} second.')
            print('The directory was sorted.')
    except (FileNotFoundError, OSError) as e:
        print(f'Error: {e}')


if __name__ == '__main__':

    start()

