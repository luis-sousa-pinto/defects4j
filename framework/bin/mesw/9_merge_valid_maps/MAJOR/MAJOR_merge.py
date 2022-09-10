import sys
import os
import csv

PID = sys.argv[1]
VID = sys.argv[2]

MAJOR_DIR = "/home/people/12309511/scratch/major_mutation_results/" + PID + "/" + VID
VALID_SUITES = "/home/people/12309511/logging/10_stats/5gte_suite_bugs/" + PID + "-" + VID + "-suites"
OUT_DIR = "/home/people/12309511/scratch/MAJOR_valid_maps/" + PID + "/" + VID
MAPS_DIR = "/home/people/12309511/scratch/major_mutation_results/" + PID + "/" + VID + "/kill_maps"
MUTANTS_LOG = "/home/people/12309511/scratch/major_mutation_results/" + PID + "/" + VID + "/mutants.log"

master = OUT_DIR + "/" + PID + "-" + VID + "-MAJOR-merged.csv"

f_master = open(master, "w")
f_suites = open(VALID_SUITES, "r")

with open(MUTANTS_LOG, "r") as f_mutants_log:
    num_mutants = len(f_mutants_log.readlines())

# Dictionary to store mutants and killing tests
mutant_dict = {}

for i in range(1, num_mutants + 1):
    mutant_dict[str(i)] = []

with f_suites:
    valid_suites_set = set()
    for line in f_suites:
        gen = line.split("-")[2]
        seed = line.split("-")[3].rstrip()

        valid_suites_set.add(gen + "-" + seed)

with f_master:

    map_dir = os.fsencode(MAPS_DIR)

    for file in os.listdir(map_dir):
        filename = os.fsdecode(file)

        gen = filename.split("-")[1]
        seed = filename.split("-")[2]
        suite = gen + "-" + seed

        # If the suite this map belongs to is valid then parse test and mutant
        if suite in valid_suites_set:
            test_class = filename.split("-")[3]
            test_method = filename.split("-")[4]

            if gen == "dev":
                killing_test = VID + "-" + gen + "-" + seed + "-" + test_class + "::" + test_method
            else:
                killing_test = VID + "-" + gen + "-" + seed + "-" + test_class + "." + test_method

            # Open map to read lines/mutants killed
            with open(os.path.join(MAPS_DIR, filename), "r") as f_map:
                for l_num, line in enumerate(f_map):
                    # Skip header
                    if l_num > 0:
                        mutant_id = line.split(",")[1]

                        mutant_dict[mutant_id] += [killing_test]

    csv_writer = csv.writer(f_master)

    for key, value in mutant_dict.items():
        mutant = key
        row = [key] + value
        csv_writer.writerow(row)
