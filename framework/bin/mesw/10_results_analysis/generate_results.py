import csv
import re

f_valid_bugs = open("/home/people/12309511/scripts/auto_gen_tests_pipeline/10_results_analysis/valid_bugs", "r")
f_report = open("/home/people/12309511/mutation_analysis/report.csv", "w")
f_report_mutators = open("/home/people/12309511/mutation_analysis/mutators.csv", "w")
f_major_mutators = open("/home/people/12309511/mutation_analysis/major_mutators.csv", "w")
f_pit_mutators = open("/home/people/12309511/mutation_analysis/pit_mutators.csv", "w")

major_dir = "/home/people/12309511/mutation_analysis/major"
pit_dir = "/home/people/12309511/mutation_analysis/pit"

MAJOR_MUTANT_OPS = ["AOR", "LOR", "COR", "ROR", "SOR", "ORU", "EVR", "LVR", "STD"]

# Removed these non existent mutators
# EmptyReturns
# FalseReturns
# TrueReturns
# NullReturns

# Removed obsolete/extended mutators
# Math
# ConditionalsBoundary
# NegateConditionals
# InlineConstant

PIT_MUTANT_OPS = ["Increments", "InvertNegs", "ReturnVals", "VoidMethodCall", "PrimitiveReturns", "ConstructorCall",
                  "NonVoidMethodCall", "RemoveConditional", "ABS", "AOR", "AOD",
                  "CRCR", "OBBN", "ROR", "UOI", "BooleanTrueReturnVals", "BooleanFalseReturnVals",
                  "ArgumentPropagation",
                  "NullReturnVals", "NakedReceiver", "MemberVariable", "EmptyObjectReturnVals", "RemoveIncrements",
                  "Switch", "RemoveSwitch", "BigInteger"]

with f_valid_bugs, f_report, f_report_mutators, f_major_mutators, f_pit_mutators:
    report_writer = csv.writer(f_report)
    mutators_writer = csv.writer(f_report_mutators)
    major_mutators_writer = csv.writer(f_major_mutators)
    pit_mutators_writer = csv.writer(f_pit_mutators)

    major_mutator_header = ["Bug-ID"]

    for each in MAJOR_MUTANT_OPS:
        major_mutator_header += [each + "-Revealing"]
        major_mutator_header += [each + "-Non-Revealing"]
        major_mutator_header += [each + "-No-Coverage"]

    major_mutators_writer.writerow(major_mutator_header)

    pit_mutator_header = ["Bug-ID"]

    for each in PIT_MUTANT_OPS:
        pit_mutator_header += [each + "-Revealing"]
        pit_mutator_header += [each + "-Non-Revealing"]
        pit_mutator_header += [each + "-No-Coverage"]

    pit_mutators_writer.writerow(pit_mutator_header)

    report_writer.writerow(["Bug-ID", "MAJOR fault-revealed", "MAJOR # revealing mutants", "MAJOR # mutants",
                            "PIT fault-revealed", "PIT # revealing mutants", "PIT # mutants",
                            "Total # revealing mutants"])

    mutators_writer.writerow(["Bug-ID", "Mutation Tool"])

    for line in f_valid_bugs:
        PID = line.split("-")[0]
        VID = line.split("-")[1]

        print(PID, VID)

        # Setup file handles

        major_stats = major_dir + "/" + PID + "/" + VID + "/stats_MAJOR"
        major_reveal = major_dir + "/" + PID + "/" + VID + "/revealing_mutants_MAJOR"
        major_non_reveal = major_dir + "/" + PID + "/" + VID + "/non_revealing_mutants_MAJOR"
        major_no_coverage = major_dir + "/" + PID + "/" + VID + "/no_coverage_mutants_MAJOR"

        pit_stats = pit_dir + "/" + PID + "/" + VID + "/stats_PIT"
        pit_reveal = pit_dir + "/" + PID + "/" + VID + "/revealing_mutants_PIT"
        pit_non_reveal = pit_dir + "/" + PID + "/" + VID + "/non_revealing_mutants_PIT"
        pit_no_coverage = pit_dir + "/" + PID + "/" + VID + "/no_coverage_mutants_PIT"

        major_stats_reader = csv.reader(open(major_stats, "r"))
        major_reveal_reader = csv.reader(open(major_reveal, "r"))
        major_non_reveal_reader = csv.reader(open(major_non_reveal, "r"))
        major_no_coverage_reader = csv.reader(open(major_no_coverage, "r"))

        pit_stats_reader = csv.reader(open(pit_stats, "r"))
        pit_reveal_reader = csv.reader(open(pit_reveal, "r"))
        pit_non_reveal_reader = csv.reader(open(pit_non_reveal, "r"))
        pit_no_coverage_reader = csv.reader(open(pit_no_coverage, "r"))

        major_revealed = False
        pit_revealed = False

        pit_revealing_list = []
        major_revealing_list = []

        for row in major_stats_reader:
            if row[0] == "Total":
                major_total_mutants = int(row[1])
            if row[0] == "Revealing":
                major_revealing = int(row[1])
                if major_revealing > 0:
                    major_revealed = True

        for row in pit_stats_reader:
            if row[0] == "Total":
                pit_total_mutants = int(row[1])
            if row[0] == "Revealing":
                pit_revealing = int(row[1])
                if pit_revealing > 0:
                    pit_revealed = True

        # Setup dicts
        mut_dict_major_revealing = {
            "AOR": 0,
            "LOR": 0,
            "COR": 0,
            "ROR": 0,
            "SOR": 0,
            "ORU": 0,
            "EVR": 0,
            "LVR": 0,
            "STD": 0
        }
        mut_dict_major_non_revealing = dict(mut_dict_major_revealing)
        mut_dict_major_no_coverage = dict(mut_dict_major_revealing)

        mut_dict_pit_revealing = {
            "Increments": 0,
            "InvertNegs": 0,
            "ReturnVals": 0,
            "VoidMethodCall": 0,
            "PrimitiveReturns": 0,
            "ConstructorCall": 0,
            "NonVoidMethodCall": 0,
            "RemoveConditional": 0,
            "ABS": 0,
            "AOR": 0,
            "AOD": 0,
            "CRCR": 0,
            "OBBN": 0,
            "ROR": 0,
            "UOI": 0,
            "BooleanTrueReturnVals": 0,
            "BooleanFalseReturnVals": 0,
            "ArgumentPropagation": 0,
            "NullReturnVals": 0,
            "NakedReceiver": 0,
            "MemberVariable": 0,
            "EmptyObjectReturnVals": 0,
            "RemoveIncrements": 0,
            "Switch": 0,
            "RemoveSwitch": 0,
            "BigInteger": 0
        }
        mut_dict_pit_non_revealing = dict(mut_dict_pit_revealing)
        mut_dict_pit_no_coverage = dict(mut_dict_pit_revealing)

        for row in major_reveal_reader:
            mut_op = row[0].split(":")[1]
            major_revealing_list += [mut_op]
            mut_dict_major_revealing[mut_op] += 1

        for row in major_non_reveal_reader:
            mut_op = row[0].split(":")[1]
            mut_dict_major_non_revealing[mut_op] += 1

        for row in major_no_coverage_reader:
            mut_op = row[0].split(":")[1]
            mut_dict_major_no_coverage[mut_op] += 1

        obsolete_mutants = 0
        obsolete_revealing_mutants = 0

        for row in pit_reveal_reader:
            s = row[0].split(".")
            mut_op = s[len(s) - 1].split("-")[0]
            mut_op_short = mut_op.split("Mutator")[0]
            mut_op_short = re.sub(r'\d+', '', mut_op_short)

            if mut_op_short not in ["Math", "ConditionalsBoundary", "NegateConditionals", "InlineConstant"]:
                pit_revealing_list += [mut_op_short]
                mut_dict_pit_revealing[mut_op_short] += 1
            else:
                print("Obsolete Revealing " + mut_op + " -- " + mut_op_short)
                obsolete_mutants += 1
                obsolete_revealing_mutants += 1

        for row in pit_non_reveal_reader:
            s = row[0].split(".")
            mut_op = s[len(s) - 1].split("-")[0]
            mut_op_short = mut_op.split("Mutator")[0]
            mut_op_short = re.sub(r'\d+', '', mut_op_short)

            if mut_op_short not in ["Math", "ConditionalsBoundary", "NegateConditionals", "InlineConstant"]:
                mut_dict_pit_non_revealing[mut_op_short] += 1
            else:
                print("Obsolete " + mut_op + " -- " + mut_op_short)
                obsolete_mutants += 1

        for row in pit_no_coverage_reader:
            s = row[0].split(".")
            mut_op = s[len(s) - 1].split("-")[0]
            mut_op_short = mut_op.split("Mutator")[0]
            mut_op_short = re.sub(r'\d+', '', mut_op_short)

            if mut_op_short not in ["Math", "ConditionalsBoundary", "NegateConditionals", "InlineConstant"]:
                mut_dict_pit_no_coverage[mut_op_short] += 1
            else:
                print("Obsolete " + mut_op + " -- " + mut_op_short)
                obsolete_mutants += 1

        report_writer.writerow([PID + "-" + VID, major_revealed, major_revealing, major_total_mutants, pit_revealed,
                                pit_revealing - obsolete_revealing_mutants, pit_total_mutants - obsolete_mutants,
                                major_revealing + (pit_revealing - obsolete_revealing_mutants)])
        mutators_writer.writerow([PID + "-" + VID, "MAJOR"] + major_revealing_list)
        mutators_writer.writerow([PID + "-" + VID, "PIT"] + pit_revealing_list)

        major_row = [PID + "-" + VID]

        for each in MAJOR_MUTANT_OPS:
            major_row += [mut_dict_major_revealing[each]]
            major_row += [mut_dict_major_non_revealing[each]]
            major_row += [mut_dict_major_no_coverage[each]]

        major_mutators_writer.writerow(major_row)

        pit_row = [PID + "-" + VID]

        for each in PIT_MUTANT_OPS:
            pit_row += [mut_dict_pit_revealing[each]]
            pit_row += [mut_dict_pit_non_revealing[each]]
            pit_row += [mut_dict_pit_no_coverage[each]]

        pit_mutators_writer.writerow(pit_row)
