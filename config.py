"""
File for path to different directories of project
"""

from pathlib import Path

# Path to project directory
PATH = Path(__file__).parent
PATH_TO_PRICE = PATH / "data" / "price.json"
PATH_TO_DATA = PATH / "data"


"""
Get params of database from database.ini
"""
from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


if __name__ == "__main__":
    print(type(PATH_TO_PRICE))