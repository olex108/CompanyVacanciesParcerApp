from pathlib import Path

from configparser import ConfigParser

"""
File for path to different directories of project
"""

# Path to project directory
PATH = Path(__file__).parent
PATH_TO_PRICE = PATH / "data" / "price.json"
PATH_TO_DATA = PATH / "data"

"""
Get params of database from database.ini
"""


def config(filename="database.ini", section="postgresql"):

    path_to_file = PATH / filename
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(path_to_file)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
