"""

Auxiliary library to store common configurable values and methods.
If required, interphases will be stored here.

"""

import json
import os
import sys


def get_platform():
    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]


# CONFIGURATION VALUES POPULATED AT RUNTIME

class Config:

    def __init__(self):
        self.LIBS_PATH = None
        self.ROOT_PATH = None

    def update(self, params):
        """
        Adds the given params as self attributes to be invoked in other modules
        :dict params: key value config combinations to be added to config
        """
        for key, value in params.items():
            setattr(self, key, value)


CONFIG = Config()


def load_config():
    """
    Loads default config and updates if necessary with the contents of the provided file
    :string config_file: path to the config file with updated values
    """
    CONFIG.HOST_OS_TYPE = get_platform()


# INITIAL SETUP METHODS
def set_up_paths(paths):
    """
    Adds the given paths to PYTHON PATH to use up globally
    @:param paths: list | list of sub-paths that need to be added to PYTHON_PATH referenced from
                the tests folder
    """
    # Set up the project path from the test directory
    CONFIG.LIBS_PATH = os.path.normpath(CONFIG.ROOT_PATH + os.sep + 'libs')
    paths = [os.path.join(CONFIG.ROOT_PATH, path) for path in paths]
    for path in paths + [CONFIG.LIBS_PATH, CONFIG.ROOT_PATH]:
        sys.path.append(path)


# PATH MANIPULATION METHODS
def get_test_data_path(subpath):
    """
        Based on a relative path from the test_data folder, returns the
        absolute path required
        @:param subpath: str | file's subpath referenced from test_data folder
        :return str

    """

    return os.path.join(CONFIG.ROOT_PATH, "test_data", subpath)


# FILE MANIPULATION METHODS
def read_file(filepath):
    """
    Reads a file and returns its content as str
    @:param filepath: str | file's path to read file
    :return str
    """
    with open(get_test_data_path(filepath), "r") as f:
        return f.read()



