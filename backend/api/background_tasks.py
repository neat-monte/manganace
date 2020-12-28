import os
import shutil


def delete_file(filepath: str):
    if os.path.exists(filepath):
        os.remove(filepath)


def delete_folder(filepath: str):
    if os.path.exists(filepath):
        shutil.rmtree(filepath)
