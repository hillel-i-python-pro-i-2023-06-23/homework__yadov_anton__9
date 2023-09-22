import pathlib

from application.config import FILES_OUTPUT_DIR
from application.services.create_file import create_file


def read_file(path: pathlib.Path = None):
    if path is None:
        path = FILES_OUTPUT_DIR / "new.txt"

    if not path.exists():
        create_file(path)

    file_to_read = read_txt(txt_file_path=path)
    return file_to_read


def read_txt(txt_file_path: pathlib.Path) -> str:
    with open(txt_file_path) as txt_file:
        text = txt_file.read()
    return text
