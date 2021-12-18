# Defects4J
Defects4J is a collection of reproducible bugs and a supporting infrastructure
with the goal of advancing software engineering research.

Refer to the [original repository](https://github.com/rjust/defects4j) for more informations, and a brief guide to how to setup the infrastructure.

# Mutation tools
The only mutation tool integrated in the original Defects4J framework is Major.

The three mutation tools added are Judy, Jumble and Pit, bumping the number of installed mutation tools to four.
These tools are installed and configured when the project is initializated; after the setup phase is completed, they are placed in `<defects4jPath>/mutation_tools`.

# Analyzer
The analyzer scripts can automate the execution of particular commands and the extraction of useful informations regarding Defects4J Project.

In the following, `<analyzerPath>` will refer to the installation folder of *Analyzer*; this is located in `<defects4jPath>/analyzer`.

## Installation
To use Analyzer, `python3` must be available in your system. You can refer to the [official download page](https://www.python.org/downloads/) or your distribution's package manager. **The minimum required version is 3.8.**

```bash
$ sudo apt install python3 python3-pip -y
$ python3 --version
Python 3.8.x
```

After ensuring that Python is installed, the required packages are next; you can install them with 
```bash
python3 -m pip install --user <analyzerPath>/requirements.txt
```

## Usage
The usage of the module is 
```bash
python3 <analyzerPath>/analyzer.py <action> <projectPath> [<flags>]
```

Check the `--help` to see all commands.

## Actions

- `backup`: Backup the current testsuite. This action is automatically performed if no backup exists.

- `restore`: Restore the backupped testsuite.

- `run`: This action will launch specified tools against the selected testsuite, collecting tool's output file(s). The default path where the output is collected is `<projectPath>/tools_output/<tool>`.

- `mutants`: This action will launch specified tools against a *dummy*, i.e. empty, test suite. This serves in reporting all the mutants generated by the tool.
PS: Judy won't generate any mutant with this method.

## Required arguments

- `action`: Must be one of the aforementioned actions.
- `path`: Must be the path of a checked out Defects4j project.

## Optional arguments

- `--tools`: Specify a list of tools (space separated) to use during the elaboration of the action.
Valid values are `judy`, `jumble`, `major`, `pit`.
If not specified, every tool will be used.

- `-t`, `--testsuite`: Specify a path to a testsuite to include in the Defects4J project test suite.
This path can lead to a single class test, or to a directory of class tests; in both case these files will be copied to the project test directory, in the same package as the relevant class.

- `--all-dev`: Run the selected action including all the developers' tests. Mutually exclusive with `--single-dev` and `--relevant-dev`. 
Defaults to false.

- `--single-dev`: Run the selected action including only the single developers' test created for the relevant class under study; by convention class `package.to.Class` will be matched with the test class `package.to.ClassTest`.
Mutually exclusive with `--all-dev` and `--relevant-dev`.
Defaults to false.

- `--relevant-dev`: run the selected action including the relevant developers' tests, found inside `<defects4jPath>/framework/projects/<project>/relevant_tests/<bug>`.
Mutually exclusive with `--with-dev` and `--with-single-dev`.
Defaults to false.

- `--skip-setup`: Skip the setup of the tool, executing the specified action against the current testsuite found in the project test folder. 

- `-v`, `--verbose`: Increase the verbosity of output.

- `--stdout`: Enable the stdout of the selected tools.

- `--stderr`: Enable the stderr of the selected tools.

## Example of usage
An example of usage is given below.

### Checkout of a project
```bash
# assure that the parent folder is existing, e.g. /tmp/d4j
mkdir -p /tmp/d4j

# checkout a Defects4J project
defects4j checkout -p Cli -v 32f -w /tmp/d4j/cli32f

# set a variable to ease reading and usage
D4J_PROJECT=/tmp/d4j/cli32f
```

### Analyzer run
```bash
# get automatically defects4j paths
D4J_HOME=$(cd $(dirname $(which defects4j))/../.. && pwd)
D4J_ANALYZER="$D4J_HOME/analyzer"

# run all four mutation tools on the project with an empty test suite
python3 $D4J_ANALYZER/analyzer.py run $D4J_PROJECT

# run the tools without modifying the current test suite
python3 $D4J_ANALYZER/analyzer.py run $D4J_PROJECT --skip-setup

# run the tools with a java test file
python3 $D4J_ANALYZER/analyzer.py run $D4J_PROJECT -t /path/to/Test.java

# run the tools with all the java test files found inside the dir
python3 $D4J_ANALYZER/analyzer.py run $D4J_PROJECT -t /path/to/testsDir

# run the tools with all the original developers java test files
python3 $D4J_ANALYZER/analyzer.py run $D4J_PROJECT --all-dev

# you can also mix the testsuites
python3 $D4J_ANALYZER/analyzer.py run $D4J_PROJECT --all-dev -t /path/to/testsDir

# run only a tool on the project
python3 $D4J_ANALYZER/analyzer.py run $D4J_PROJECT --tools jumble

# run the tools capturing also their stdout and stderr
python3 $D4J_ANALYZER/analyzer.py run $D4J_PROJECT --stdout --stderr
```

# Reports Analyzer
The report analyzer script can extract informations about mutation tools' output files, making them reports. Each report is a collection of useful informations, like the total count of mutations generated, the mutation score, or even the mutations themselves.

## Usage
The usage of the module is 
```bash
python3 <analyzerPath>/reportsanalyzer.py <command> -p <projectName> -b <projectBug> -t <toolName> <reportPath> [<reportPath> ...] [<commandFlags>]
```
Check the `--help` to see all commands.

The options `-p`, `-b` and `-t` are shared by all commands, thus they are required also by the CLI.

## Required arguments
- `command`: The command to execute on the list of reports; a more detailed description is available below.

- `-p <projectName>`: Must be the name of a Defects4j project; this is the exact name used when `defects4j checkout` is called, e.g. *Cli*, *Gson* and *Lang*.

- `-b <projectBug>`: Must be the identifier of a Defects4j project's bug; this is the exact bug id used when `defects4j checkout` is called, except that the bug status, i.e. buggy `b` or fixed `f`, is omitted.

- `-t <toolName>`: Must be the name of a mutation tool; this is expected lowercase, and can be one in `judy`, `judylog`, `jumble`, `major` and `pit`.

- `reportPath`: The path to a report; this has to be a single file if the chosen mutation tool is a `SingleFileReport`, otherwise a directory containing two or more files if the mutation tool is a `MultipleFilesReport`.

### Expected `reportPath`
As explained before, a report can be made of one or two (or more) files. 

**Major** report is classified as **`MultipleFilesReport`**, because *Analyzer* generates two output file for a single execution.

**Jumble and Pit** are classified as **`SingleFileReport`**, because *Analyzer* generates only one output file for each tool for every execution.

**Judy**, however, is classified both as **`SingleFileReport`** and **`MultipleFilesReport`**; *Analyzer* generates two output file for a single execution, but the count of parsed killed mutations is different from count of generated and killed mutations, so the tester has the possibility of using both version of the same report.

- When dealing with `SingleFileReport` tools, `reportPath` has to be provided as the single **file** generated.
- When dealing with `MultipleFilesReport`, `reportPath` has to be provided as the **directory** containing the two or more files required to be parsed as a single report.

#### What to provide for each tool
The reported filenames lister below are the original names of the files, as they are collected by *Analyzer*; these names can be different, but the extension must match the one reported.

- JudyLog) Judy directory must contain both one *json* file and one *log* file, that are respectively `result.json` and `judy.log`.

- Judy) Judy file must the *json* file, that is `result.json`.

- Jumble file must be the *txt* file, that is `jumble_output.txt`.

- Major directory must contain both one *csv* file and one *log* file, that are respectively `kill.csv` and `mutants.log`.

- Pit file must be the *xml* file, that is `mutations.xml`.


## Optional arguments
They are specific for each command, hence they are reported together with them.

## Commands
As said before, three options are mandatory and shared between commands; each command, however, can have from 0 up to *N* optional arguments.


### `summary`
This command prints the summary of every report provided as input. 

A **summary** is a collection of information about a report; it shows the report hash, the timestamp of creation, the class under mutation, the count of mutants generated, killed and alive, the calculated mutation score, and (if possible) the complete printout of the mutants, with all their information.

An example of `summary` output is reported below:
```
JumbleReport Summary [Hash: 51ab6dbaf66b45fca1b6bf1bc304be21]
Report created at:    2021-10-09 14:29:03.834219
Mutated class:        org.apache.commons.cli.HelpFormatter
Total mutants count:  245
Killed mutants count: 244
Live mutants count:   1
Mutation score:       0.9959183673469387
Cannot report Killed mutants
Live mutants report:
< SNIP >
Filepath: ../work/cli32f/tools_output/jumble/jumble2.txt
```

#### Optional arguments
- `--full`: Shows also the complete printout of the mutants; if not specified, the printout is omitted.


### `table`

This command prints the table of mutations, where each row identify a different mutation, and each column is a report provided as input. The default list of mutations to use are the live mutations.

If the list of mutations is available, then for every cell it will be displayed the `hash_dict` of the mutant, i.e. the unique set of attributes that makes unique a mutant in a set of mutants.
A `NaN` is displayed when a report is missing that mutation from its set.

An example of `table` output is reported below:
```
              51ab6dba      ede34a30
Mutant                          
41f94599         {...}           NaN
f2c32c16           NaN         {...}
```

#### Optional arguments
- `--killed`: Displays killed mutations instead of live mutations as index.
- `-o OUTPUT`, `--output OUTPUT`: Saves the table in a *csv* file named `OUTPUT`, instead of displaying it on `stdout`.


### `effectiveness`
Compute the *effectiveness* of one or more reports when compared to a base report, thus **requiring two or more input reports**.

Effectiveness is defined as one minus the count of live mutations of a report divided by the total count of live mutations (or, the count of live mutations of base report). Every other report *should* be produced with the testsuite used by the base report, combined with another test suite, so that it won't exist a live mutation in report *i* that doesn't belong to base report.

__This command shows the effectiveness of the *other* test suite in killing *base* live mutations.__

An example of `effectiveness` output is reported below:

```
          live_count  live_total_count  effectiveness
2007a983          28                28       0.000000
e91feb39          26                28       0.071429
```

#### Optional arguments
- `--base-index BASE_INDEX`: The zero-based index of the report to use as base in the list of provided reports. If missing or negative, the first will be used; if too big, the last will be used.

- `-o OUTPUT`, `--output OUTPUT`: Saves the table in a *csv* file named `OUTPUT`, instead of displaying it on `stdout`.

## Example of usage
An example of usage is given below. The execution of *ReportsAnalyzer* should be subsequent to *Analyzer*.

### ReportsAnalyzer run
```bash
# get automatically paths
D4J_HOME=$(cd $(dirname $(which defects4j))/../.. && pwd)
D4J_ANALYZER="$D4J_HOME/analyzer"

# get the summary of a Judy report
python3 $D4J_ANALYZER/reportsanalyzer.py summary \
-p Cli -b 32 -t judy /path/to/judy/result.json

# get the effectiveness of a Jumble report with respect to its base report
python3 $D4J_ANALYZER/reportsanalyzer.py effectiveness -p Cli -b 32 -t jumble \
/path/to/jumble/base_jumble_output.txt \
/path/to/jumble/jumble_output.txt
```
