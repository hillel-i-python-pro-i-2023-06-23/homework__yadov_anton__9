import pathlib
from typing import Final

ROOT_DIR: Final[pathlib.Path] = pathlib.Path(__file__).parents[1]
FILES_OUTPUT_DIR: Final[pathlib.Path] = ROOT_DIR.joinpath("files_output")
DB_PATH: Final[pathlib.Path] = ROOT_DIR.joinpath("db", "db.sqlite")
