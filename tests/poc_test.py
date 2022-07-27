import pytest
import glob
import os.path

from libs import builtins
from libs.consts import OS, naming_convention
from libs.fixtures.common_fixtures import run_cmd, aux_validation

INPUT_FILES = [x for x in glob.glob(os.path.join(
    builtins.get_test_data_path(OS.get(builtins.CONFIG.HOST_OS_TYPE)), '*.csv'))
               if "_exp_" not in x]

SEARCH_CRITERIA = list(naming_convention.keys())

EXPECTED = {f: {c: [x for x in glob.glob(os.path.join(
    builtins.get_test_data_path(OS.get(builtins.CONFIG.HOST_OS_TYPE)), '*.csv'))
                    if naming_convention.get(c, None) in x and f.replace(".csv", '') in x]
                for c in SEARCH_CRITERIA} for f in INPUT_FILES}


class TestClassPOC:

    @pytest.mark.parametrize("input_file", INPUT_FILES)
    @pytest.mark.parametrize("criteria", SEARCH_CRITERIA)
    def test_case_combinations(self, run_cmd, input_file, criteria, aux_validation):
        # Execute cmd command for given file and criteria
        outcome = run_cmd(input_file, criteria)

        # Check if input file exists and validate returned code
        if os.path.isfile(input_file):
            assert outcome.returncode == 0
        else:
            assert outcome.returncode == 2

        # Check expected file before make the comparison.
        try:
            expected = EXPECTED.get(input_file).get(criteria)
            assert len(expected) == 1
        except AssertionError:
            # Xfailing test since there is no expected file for the given combination
            if len(expected) == 0:
                pytest.xfail(f"No expected file for given combination: \"{input_file.split(os.sep)[-1]}\" | \"{criteria}\"")
            # Xfailing test since there is more than one expected file for the given combination | corrupted test data
            elif len(expected) > 1:
                pytest.xfail(f"Test data needs to be reviewed, there is more than one file for combination: "
                             f"\"{input_file.split(os.sep)[-1]}\" | \"{criteria}\"")

        # Validate cmd execution result against expected data
        try:
            assert builtins.read_file(expected[0]) == outcome.stdout
        except AssertionError as e:
            # Extra handling for not matching cases
            if not aux_validation(file_to_validate=input_file, criteria=criteria, cmd_outcome=outcome.stdout):
                # raise assertion error since the cmd output is wrong
                raise e
            else:
                # Xfailing test since the cmd output is correct beyond that the comparison has failed.
                # Issue related with corrupted test data
                pytest.xfail(f"System is working as expected, file containing expected results needs to be reviewed: "
                             f"\"{expected[0].split(os.sep)[-1]}\"")
