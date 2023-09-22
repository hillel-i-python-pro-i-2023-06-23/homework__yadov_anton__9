import pathlib

from application.config import FILES_OUTPUT_DIR


def create_file(file_path: pathlib.Path = None) -> pathlib.Path:
    if file_path is None:
        file_path = FILES_OUTPUT_DIR.joinpath("new.txt")

    with file_path.open("w") as new_file:
        new_file.write("This is new generated file.")

    return file_path
