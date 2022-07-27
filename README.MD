# ECelona POC Automation Framework

## Requirements

- Python 3
- Git
- OS dependencies
- All Python library dependencies (included in *requirements.txt*).


## Installation

To deploy the tool:

1. Clone the repository.
2. Start of by installing the correct dependencies into a virtual environment within the submodule named "**.env**".

```shell
    cd $PROJECT_ROOT_PATH
    python -m venv .env
    source .env/bin/activate
```
3. Make sure that all dependencies are satisfied.
    - To install dependencies run manually:
        ```shell
        pip install -r requirements.txt
        ```
4. Test everything works by running a test `python runner.py -t $testpath`.
      - Do not forget to activate the env first (details below)

## Run tests

1. From project path root, run on terminal:
    ```shell
    source .env/bin/activate
    python tcrunner.py -t $testpath 
    ```

2. Additional arguments can be used to filter the tests being run:

```
usage: tcrunner.py [-h] [-t TESTPATH] [-f FILTER]

optional arguments:
  -h, --help            show this help message and exit
  -t TESTPATH, --testpath TESTPATH
                        Relative path in which to find tests
  -f FILTER, --filter FILTER
                        String to filter tests by name

```

For example, to run all test cases contained on a class, run:

```
python tcrunner.py -t tests/api -f TestWorkflowsEdgeCases
```

To run a specific test (test case name refers to test function name):

```
-t tests/api -f test_get_workflows_empty_params
```

To run a set of tagged tests run:

```
-t tests/api -m smoke
```

Also name and tag filters can be combined

```
-t tests/api -f TestWorkflowsEdgeCases -m smoke
```
  
## Code structure

1. runner.py (the entry point)
2. Libs folder

### runner.py
The code is structured to use `runner.py` as the entry point script and uses Pytest to tun tests. It handles paths for test execution, together with any additional functionality that adds upon pytest.

### Libs

Test cases make use of fixtures. Within `libs.fixtures.common_fixtures.py`, fixtures that are source agnostic or that can be reused can be placed so as not to bloat test cases. The same principle applies to `libs.builtins.py` but for methods. This makes the import process easier when the test cases are written since the imports are included in the template.  

## Reporting and Browsing results

Test cases produce xml results that are placed into the results folder. 
