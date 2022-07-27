import subprocess
import pytest
from libs.consts import naming_convention
from libs import builtins
import os.path
import re


@pytest.fixture(scope="module")
def run_cmd():
    """
    Wrapper that executes cmd commands for both OS
    :return: function
    """
    def _unix(file, criteria):
        """
        Execute grep command and returns the result
        :param file: str | absolute path of input file
        :param criteria: str | search pattern
        :return: <class 'subprocess.CompletedProcess'>
        """
        bash_command = f"grep -E \"{criteria}|^date\" {file}"
        result = subprocess.run(bash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        return result

    def _win():
        """
        Execute Win commands and returns the result, not implemented yet
        """
        return "NOT implemented"

    if builtins.CONFIG.HOST_OS_TYPE == 'linux':
        return _unix
    # NOT IMPLEMENTED
    else:
        return _win


@pytest.fixture(scope="module")
def aux_validation():
    """
    Wrapper that returns aux validation method
    :return: function _aux
    """
    def _aux(file_to_validate, criteria, cmd_outcome):
        """
        Aux validation
        Validates the actual outcome of the grep execution in case that a test fails, this extra validation
        was applied to avoid false positives.
        :param file_to_validate: str
        :param criteria: str
        :param cmd_outcome: str
        :return: bool | True if system is working as expected - False if the failure is cause of the Automated test case
        """
        with open(file_to_validate, "r") as f:
            qa_validation = f"".join([l for l in f.readlines() if re.search(f"{criteria}|^date", l)])
        if qa_validation == cmd_outcome:
            return True
        else:
            return False

    return _aux
