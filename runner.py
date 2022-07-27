"""

Test Case Runner (tcrunner.py)

Entry point for test caseses.

This file is used to set up configuration for testcase running and logging.
It will also include additional functionality related to reporting and CI.

"""
import sys
import os, inspect
import pytest
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from libs import builtins

DESCRIPTION = f"""
  Test Case Runner (tcrunner) 

  Developed by Ezequiel Celona for Patagonian's Code challange
  
"""


def run_tests(args):
    """
        Main runner for pytest test cases.
    """
    pytest_args = ["-vv", "-rA", "--disable-warnings", "--junitxml=./results/out_report.xml", "-o junit_logging=all", args.testpath]
    if args.filter:
        pytest_args = ["-k", args.filter] + pytest_args
    if args.tag:
        pytest_args = ["-m", args.tag] + pytest_args
    return pytest.main(pytest_args)


def main():
    # Common Paths to the applications. This is an anchor.
    # If an entrypoint is introduced, the reference might be moved to the PROJECT PATH
    builtins.CONFIG.ROOT_PATH = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe())))

    # Additional Paths referenced from anchor
    builtins.set_up_paths(["tests", "test_data", "libs"])

    # Set up configuration
    builtins.load_config()

    # Set up Argparser
    parser = ArgumentParser(description=DESCRIPTION,
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('-t', '--testpath',
                        dest='testpath',
                        help="Path in which to find tests",
                        default="tests")

    parser.add_argument('-f', '--filter',
                        dest="filter",
                        help="String to filter tests by name",
                        default=None)

    parser.add_argument('-m', '--metatags',
                        dest="tag",
                        help="String to filter tests by tag",
                        default=None)

    # Process arguments
    args = parser.parse_args()

    # Run tests
    return (run_tests(args))


if __name__ == "__main__":
    sys.exit(main())

