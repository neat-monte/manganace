import os


def delete_file(filepath: str):
    if os.path.exists(filepath):
        os.remove(filepath)
