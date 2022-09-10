import subprocess
import sys
import csv


def triggering_test(test):
    # Parse test - Check if Dev and modify name
    if "dev-dev" in test:
        test = test.split("-")[3]

        # Check Dev T test file
        return test in open(DEV_TRIGGERING_TEST_FILE).read()
    else:
        # Check T test file
        return test in open(TRIGGERING_TEST_FILE).read()


def revealing_mutant(row):

    # Don't account for empty col after last ',' hence length - 1
    for i in range(1, len(row), 1):
        test = row[i]

        # Check if triggering
        if not triggering_test(test):
            return False
    return True


def get_mutant_name(mutant_id):
    fh = open(MAJOR_MUTANT_FILE)
    for line_number, line in enumerate(fh):
        if line_number + 1 == int(mutant_id):
            return line
    return ""


PID = sys.argv[1]
VID = sys.argv[2]

# Identify MAJOR map file, MAJOR mutants file, triggering test file, dev triggering test file e.g triggering_tests/Cli/10f/Cli-10f-triggering_tests
MAJOR_MAP_FILE = "/home/people/12309511/scratch/MAJOR_valid_maps/" + PID + "/" + VID + "/" + PID + "-" + VID + "-MAJOR-merged.csv"
MAJOR_MUTANT_FILE = "/home/people/12309511/scratch/MAJOR_valid_maps/" + PID + "/" + VID + "/" + PID + "-" + VID + "-mutants.log"
TRIGGERING_TEST_FILE = "/home/people/12309511/triggering_tests/" + PID + "/" + VID + "/" + PID + "-" + VID + "-triggering_tests"
DEV_TRIGGERING_TEST_FILE = "/home/people/12309511/dev_triggering_tests/" + PID + "/" + VID + "/" + PID + "-" + VID + "-triggering_tests"

# File locations to write results to
MAJOR_REVEALING = "/home/people/12309511/mutation_analysis/major/" + PID + "/" + VID + "/revealing_mutants_MAJOR"
MAJOR_NON_REVEALING = "/home/people/12309511/mutation_analysis/major/" + PID + "/" + VID + "/non_revealing_mutants_MAJOR"
MAJOR_NO_COVERAGE = "/home/people/12309511/mutation_analysis/major/" + PID + "/" + VID + "/no_coverage_mutants_MAJOR"
MAJOR_STATISTICS = "/home/people/12309511/mutation_analysis/major/" + PID + "/" + VID + "/stats_MAJOR"

subprocess.call(['mkdir', '--parents', "/home/people/12309511/mutation_analysis/major/" + PID + "/" + VID])

f_MAJOR_map = open(MAJOR_MAP_FILE, "r")
f_MAJOR_REVEALING = open(MAJOR_REVEALING, "w")
f_MAJOR_NON_REVEALING = open(MAJOR_NON_REVEALING, "w")
f_MAJOR_NO_COVERAGE = open(MAJOR_NO_COVERAGE, "w")
f_MAJOR_STATISTICS = open(MAJOR_STATISTICS, "w")

with f_MAJOR_map, f_MAJOR_REVEALING, f_MAJOR_NON_REVEALING, f_MAJOR_NO_COVERAGE, f_MAJOR_STATISTICS:
    MAJOR_map_reader = csv.reader(f_MAJOR_map)

    total_mutants = 0
    revealing_mutants = 0
    non_revealing_mutants = 0
    no_coverage_mutants = 0

    # Iterate mutants in map
    for mutant in MAJOR_map_reader:

        if len(mutant) < 1:
            continue

        mut_id = mutant[0]
        mut_name = get_mutant_name(mut_id)
        total_mutants += 1

        if len(mutant) == 1:
            # No killing tests
            no_coverage_mutants += 1
            f_MAJOR_NO_COVERAGE.write(mut_name)
            continue

        if revealing_mutant(mutant):
            # If mutant exclusively killed by t_tests then write so
            revealing_mutants += 1
            f_MAJOR_REVEALING.write(mut_name)
        else:
            non_revealing_mutants += 1
            f_MAJOR_NON_REVEALING.write(mut_name)

    f_MAJOR_STATISTICS.write("Total," + str(total_mutants) + "\n")
    f_MAJOR_STATISTICS.write("Revealing," + str(revealing_mutants) + "\n")
    f_MAJOR_STATISTICS.write("Non-Revealing," + str(non_revealing_mutants) + "\n")
    f_MAJOR_STATISTICS.write("No Coverage," + str(no_coverage_mutants) + "\n")

    print("MAJOR STATISTICS")
    print("Total Mutants:", total_mutants)
    print("Revealing:", revealing_mutants)
    print("Non-Revealing:", non_revealing_mutants)
    print("No Coverage:", no_coverage_mutants)
