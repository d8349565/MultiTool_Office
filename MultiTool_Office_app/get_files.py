import os


def list_files(start_path,flag=''):
    for entry in os.scandir(start_path):
        if entry.is_dir():
            yield from list_files(entry.path)
        else:
            yield entry.path


def list_dirs(start_path):
    for entry in os.scandir(start_path):
        if entry.is_dir():
            yield entry.name
