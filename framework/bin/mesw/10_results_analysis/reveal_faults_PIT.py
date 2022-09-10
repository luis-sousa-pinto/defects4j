import subprocess
import sys
import csv


def triggering_test(test):
    # Parse test - Check if Dev or Randoop and modify name

    if "dev-dev" in test:
        test = test.split("-")[3]
        test = test.split("(")[0]
        s = test.split(".")
        test_method = s[len(s) - 1]
        test_class = ".".join(s[0:len(s) - 1])
        test = test_class + "::" + test_method

        # Check Dev T test file
        return test in open(DEV_TRIGGERING_TEST_FILE).read()

    elif "randoop" in test:
        test = test.split("(")[0]

    return test in open(TRIGGERING_TEST_FILE).read()


def revealing_mutant(row):

    for i in range(1, len(row), 1):
        test = row[i]

        # Check if triggering
        if not triggering_test(test):
            return False

    return True


PID = sys.argv[1]
VID = sys.argv[2]

# Identify PIT map file, triggering test file, dev triggering test file e.g triggering_tests/Cli/10f/Cli-10f-triggering_tests
PIT_MAP_FILE = "/home/people/12309511/scratch/PIT_valid_maps/" + PID + "/" + VID + "/" + PID + "-" + VID + "-PITmerged.csv"
TRIGGERING_TEST_FILE = "/home/people/12309511/triggering_tests/" + PID + "/" + VID + "/" + PID + "-" + VID + "-triggering_tests"
DEV_TRIGGERING_TEST_FILE = "/home/people/12309511/dev_triggering_tests/" + PID + "/" + VID + "/" + PID + "-" + VID + "-triggering_tests"

# File locations to write results to
PIT_REVEALING = "/home/people/12309511/mutation_analysis/pit/" + PID + "/" + VID + "/revealing_mutants_PIT"
PIT_NON_REVEALING = "/home/people/12309511/mutation_analysis/pit/" + PID + "/" + VID + "/non_revealing_mutants_PIT"
PIT_NO_COVERAGE = "/home/people/12309511/mutation_analysis/pit/" + PID + "/" + VID + "/no_coverage_mutants_PIT"
PIT_STATISTICS = "/home/people/12309511/mutation_analysis/pit/" + PID + "/" + VID + "/stats_PIT"

subprocess.call(['mkdir', '--parents', "/home/people/12309511/mutation_analysis/pit/" + PID + "/" + VID])

f_PIT_map = open(PIT_MAP_FILE, "r")
f_PIT_REVEALING = open(PIT_REVEALING, "w")
f_PIT_NON_REVEALING = open(PIT_NON_REVEALING, "w")
f_PIT_NO_COVERAGE = open(PIT_NO_COVERAGE, "w")
f_PIT_STATISTICS = open(PIT_STATISTICS, "w")

with f_PIT_map, f_PIT_REVEALING, f_PIT_NON_REVEALING, f_PIT_NO_COVERAGE, f_PIT_STATISTICS:
    PIT_map_reader = csv.reader(f_PIT_map)

    total_mutants = 0
    revealing_mutants = 0
    non_revealing_mutants = 0
    no_coverage_mutants = 0

    # Iterate mutants in map
    for mutant in PIT_map_reader:

        # Empty row - Shouldn't happen
        if len(mutant) < 1:
            continue

        mut_id = mutant[0]
        total_mutants += 1

        if len(mutant) == 1:
            # No killing tests
            no_coverage_mutants += 1
            f_PIT_NO_COVERAGE.write(mut_id + "\n")
            continue

        if revealing_mutant(mutant):
            # If mutant exclusively killed by t_tests then write so
            revealing_mutants += 1
            f_PIT_REVEALING.write(mut_id + "\n")
        else:
            non_revealing_mutants += 1
            f_PIT_NON_REVEALING.write(mut_id + "\n")

    f_PIT_STATISTICS.write("Total," + str(total_mutants) + "\n")
    f_PIT_STATISTICS.write("Revealing," + str(revealing_mutants) + "\n")
    f_PIT_STATISTICS.write("Non-Revealing," + str(non_revealing_mutants) + "\n")
    f_PIT_STATISTICS.write("No Coverage," + str(no_coverage_mutants) + "\n")

    print("PIT STATISTICS")
    print("Total Mutants:", total_mutants)
    print("Revealing:", revealing_mutants)
    print("Non-Revealing:", non_revealing_mutants)
    print("No Coverage:", no_coverage_mutants)
