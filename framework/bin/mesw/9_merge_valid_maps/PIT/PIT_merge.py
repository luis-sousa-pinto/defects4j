import sys
import re
import csv

PID = sys.argv[1]
VID = sys.argv[2]

PIT_DIR = "/home/people/12309511/scratch/pit_mutation_results/" + PID + "/" + VID
VALID_SUITES = "/home/people/12309511/logging/10_stats/5gte_suite_bugs/" + PID + "-" + VID + "-suites"
OUT_DIR = "/home/people/12309511/scratch/PIT_valid_maps/" + PID + "/" + VID
LOG_DIR = "/home/people/12309511/logging/11_PIT_merge"

master = OUT_DIR + "/" + PID + "-" + VID + "-PITmerged.csv"

f_master = open(master, "w")
f_suites = open(VALID_SUITES, "r")

with f_master, f_suites:
    mutant_dict = {}

    for line in f_suites:

        gen = line.split("-")[2]
        seed = line.split("-")[3].rstrip()

        suite_map = PIT_DIR + "/" + VID + "-" + gen + "-" + seed + "-mutations.xml"

        with open(suite_map, "r") as f_map:
            for l_num, lin in enumerate(f_map):
                if l_num >= 2:

                    try:
                        t_class = re.search(r'<mutatedClass>(.*)</mutatedClass>', str(lin)).group(1)
                        t_method = re.search(r'<mutatedMethod>(.*)</mutatedMethod>', str(lin)).group(1)
                        number = re.search(r'<lineNumber>(.*)</lineNumber>', str(lin)).group(1)
                        mut = re.search(r'<mutator>(.*)</mutator>', str(lin)).group(1)
                        idx = re.search(r'<index>(.*)</index>', str(lin)).group(1)
                        block = re.search(r'<block>(.*)</block>', str(lin)).group(1)

                        mut_id = t_class + "-" + t_method + "-" + number + "-" + mut + "-" + idx + "-" + block

                        if mut_id not in mutant_dict:
                            mutant_dict[mut_id] = []

                        killing_tests = re.search(r'<killingTests>(.*)</killingTests>', str(lin)).group(1)

                        if len(killing_tests) > 0:
                            test_array = killing_tests.split("|")
                            cleaned_test_array = []

                            suffix = VID + "-" + gen + "-" + seed + "-"

                            for test in test_array:
                                t = test.split("(")[0]
                                cleaned_test = suffix + t
                                cleaned_test_array.append(cleaned_test)

                            # Append to mut key hashmap
                            mutant_dict[mut_id] += cleaned_test_array

                    except AttributeError as e:
                        continue

    csv_writer = csv.writer(f_master)

    for key, value in mutant_dict.items():
        mutant = key
        row = [key] + value
        csv_writer.writerow(row)
