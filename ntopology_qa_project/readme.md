# ntopology QA assignment

nTopology's product is a native desktop application. We invest heavily in integration test suites (a.k.a "automated tests") 
that evaluate end-to-end behavior of the application-under-test. 

These automated tests exercise the native application via a command line interface, 
passing input files and parameters that the application uses to generate an output.

## command line application example

To better illustrate this, we model nTopology's application-under-test through a representative: the [grep](https://en.wikipedia.org/wiki/Grep) command line application. 
As an example, consider executing the following in Windows' command prompt or a Linux bash terminal:
```commandline
grep -E "some regexp" input.txt > result.txt
```

The above command takes `input.txt` as an input file, and `"some regexp""` as command line arguments. 
In layman terms, the command instructs grep to:
- read the `input.txt` file
- output any lines that match the "some regexp" regular expression.
- redirect all outut to a file called `output.txt`

**Note:** If you want to use grep on windows, an easy way is to install git for windows with "Git Bash" that contains handy unix utilities in it.

## nTopology's approach to integration tests

Our automated tests contain a large number of test cases that consists of assembling a text fixture with fixed inputs, 
running a command line application like the previous example,
then verifying that the command's results (both the executable's return code and generated outputs) match expectations.

## Example QA project

To better illustrate our approach, we provide here an example data set and a specification for integrated test suite for the **grep** application mentioned above.

Assume a set of input csv files with a format like:
```csv
date,name,event
2020/07/01,Bart Simpson,Went skating.
2021/01/01,Lisa Simpson,Learned sculpting.
2021/01/02,Maggie Simpson,"Said ""Daddy is tall"""
```
That is, a csv with tree columns. We want to evaluate how `grep` processes these text files with command line executions like:
```csv
grep -E "Maggie Simpson|^date" data/win_sample_1.csv > results/win_sample_1_res_maggie.csv
```

We have a universe of test data defined as such:
- a `data` folder in this project with fixed inputs and expected results of specific command line executions
    - input files: `win_sample_1.csv` and `win_sample_2.csv` 
    - expected files: contain the expected results of running grep with queries like `-E "${CHARACTER_NAME}|^date"` so that:
        - for every `${INPUT_FILE}`, we ran the following query and stored it in:
            - `Homer J. Simpson` in `data\${INPUT_FILE}_exp_homer.csv`
            - `Marge Simpson` in `data\${INPUT_FILE}_exp_marge.csv`
            - `Maggie Simpson` in  `data\${INPUT_FILE}_exp_maggie.csv`
            - `Ned Flanders` in `data\${INPUT_FILE}_exp_ned.csv`
- `data` folder contains an alternative set of files prefixed with `unix_` and are appropriately encoded for UNIX-like operative systems.
- Input and output files are csv's with UTF-8 contents.

To frame technical interviews, we propose **you** to create an automated test framework that has the following requirements:
- can be exercised in one OS of the following OS's: Windows or Linux.
- contains a parametrized test case that iterates over all input files with the four possible character names in the `-E "${CHARACTER_NAME}|^date"` grep query.
   - verifies that the return code is `0` for input files that exist
   - verifies that the return code is `2` for the case of input files that do not exist
- Documents all test fixtures, test framework setup and how to run it.
- verify that the results match the relevant expectations in the OS.
    - One particular combination of the test parameters yields a failing case. Discuss what this might mean, and what would you do about it.

Stretch goals:
- Done in python and pytest.
- Outputs a Junit xml report.
- Propose how to make the test more manageable if we wanted to support both Linux and Windows.




