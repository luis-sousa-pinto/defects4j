import csv
import re

f_valid_bugs = open("/home/people/12309511/scripts/auto_gen_tests_pipeline/10_results_analysis/valid_bugs", "r")
f_dist_report = open("/home/people/12309511/mutation_analysis/distances.csv", "w")

major_dir = "/home/people/12309511/mutation_analysis/major"
pit_dir = "/home/people/12309511/mutation_analysis/pit"

projects = "/home/people/12309511/defects4j/framework/projects"

with f_valid_bugs, f_dist_report:
    report_writer = csv.writer(f_dist_report)

    header = ["Bug-ID", "Mutation Tool", "Revealing", "Mutation ID", "Distance"]
    report_writer.writerow(header)

    for line in f_valid_bugs:
        PID = line.split("-")[0]
        VID = line.split("-")[1]
        num = VID.split("f")[0]

        # print(PID, VID, num)

        rows = []

        # PATCH file
        patch = projects + "/" + PID + "/patches/" + num + ".src.patch"
        f_patch = open(patch, "r")

        patch_block_tuples = []

        with f_patch:
            for line2 in f_patch:
                if re.match(r"@@.+?@@", line2):
                    blk_header = line2.split("@@")[1]
                    updated = blk_header.split("+")[1]
                    blk_start, length = updated.split(",")
                    # print(blk_start, str(int(blk_start) + int(length)))
                    patch_block_tuples.append((blk_start, int(blk_start) + int(length)))

        # print(patch_block_tuples)

        # MAJOR
        major_reveal = major_dir + "/" + PID + "/" + VID + "/revealing_mutants_MAJOR"
        f_major_reveal = open(major_reveal, "r")

        for row in f_major_reveal:
            # Remove quoted colons
            # s = re.sub(r'(?!(([^"]*"){2})*[^"]*$):', '', row)

            mut_id = row.split(":")[0]
            line_number = row.split(":")[5]
            try:
                line_number = int(line_number)
            except ValueError:
                try:
                    line_number = int(row.split(":")[6])
                except ValueError:
                    line_number = int(row.split(":")[7])

            # print(mut_id, line_number)

            try:
                distance = 10000000
                for t in patch_block_tuples:
                    if int(t[0]) <= int(line_number) <= int(t[1]):
                        distance = 0
                        break
                    else:
                        dist_start = abs(int(t[0]) - int(line_number))
                        dist_end = abs(int(t[1]) - int(line_number))
                        closest = min(dist_start, dist_end)
                        distance = min(distance, closest)
            except ValueError:
                distance = None

            rows.append([PID + "-" + VID, "Major", True, mut_id, distance])
            # print("R - Distance is", str(distance))

        major_non_reveal = major_dir + "/" + PID + "/" + VID + "/non_revealing_mutants_MAJOR"
        f_major_non_reveal = open(major_non_reveal, "r")

        for row in f_major_non_reveal:
            # Remove quoted colons
            # s = re.sub(r'(?!(([^"]*"){2})*[^"]*$):', '', row)

            mut_id = row.split(":")[0]
            line_number = row.split(":")[5]
            try:
                line_number = int(line_number)
            except ValueError:
                try:
                    line_number = int(row.split(":")[6])
                except ValueError:
                    line_number = int(row.split(":")[7])

            # print(mut_id, line_number)

            try:
                distance = 10000000
                for t in patch_block_tuples:
                    if int(t[0]) <= int(line_number) <= int(t[1]):
                        distance = 0
                        break
                    else:
                        dist_start = abs(int(t[0]) - int(line_number))
                        dist_end = abs(int(t[1]) - int(line_number))
                        closest = min(dist_start, dist_end)
                        distance = min(distance, closest)

            except ValueError:
                distance = None

            rows.append([PID + "-" + VID, "Major", False, mut_id, distance])
            # print("Non-R - Distance is", str(distance))

        # Write MAJOR
        report_writer.writerows(rows)

        rows = []

        # PIT
        pit_reveal = pit_dir + "/" + PID + "/" + VID + "/revealing_mutants_PIT"
        f_pit_reveal = open(pit_reveal, "r")

        obsolete_PIT_mutants = ["Math", "ConditionalsBoundary", "NegateConditionals", "InlineConstant"]

        for row in f_pit_reveal:
            s = row.split(".")
            mut_op = s[len(s) - 1].split("-")[0]

            mut_id = row
            mut_id = mut_id.rstrip()
            mut_id = mut_id.strip('"')
            line_number = row.split("-")[2]
            # print(mut_id, line_number)

            if any(x in mut_op for x in obsolete_PIT_mutants):
                continue
            else:
                try:
                    distance = 10000000
                    for t in patch_block_tuples:
                        if int(t[0]) <= int(line_number) <= int(t[1]):
                            distance = 0
                            break
                        else:
                            dist_start = abs(int(t[0]) - int(line_number))
                            dist_end = abs(int(t[1]) - int(line_number))
                            closest = min(dist_start, dist_end)
                            distance = min(distance, closest)

                except ValueError:
                    distance = None

                rows.append([PID + "-" + VID, "PIT", True, str(mut_id), distance])
                # print("R - Distance is", str(distance))

        pit_non_reveal = pit_dir + "/" + PID + "/" + VID + "/non_revealing_mutants_PIT"
        f_pit_non_reveal = open(pit_non_reveal, "r")

        for row in f_pit_non_reveal:
            s = row.split(".")
            mut_op = s[len(s) - 1].split("-")[0]

            mut_id = row
            mut_id = mut_id.rstrip()
            mut_id = mut_id.strip('"')
            line_number = row.split("-")[2]
            # print(mut_id, line_number)

            if any(x in mut_op for x in obsolete_PIT_mutants):
                continue
            else:
                try:
                    distance = 10000000
                    for t in patch_block_tuples:
                        if int(t[0]) <= int(line_number) <= int(t[1]):
                            distance = 0
                            break
                        else:
                            dist_start = abs(int(t[0]) - int(line_number))
                            dist_end = abs(int(t[1]) - int(line_number))
                            closest = min(dist_start, dist_end)
                            distance = min(distance, closest)

                except ValueError:
                    distance = None

                rows.append([PID + "-" + VID, "PIT", False, str(mut_id), distance])
                # print("Non-R - Distance is", str(distance))

        report_writer.writerows(rows)
