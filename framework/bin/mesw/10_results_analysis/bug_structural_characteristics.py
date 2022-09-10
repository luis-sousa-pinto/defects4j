import csv

f_valid_bugs = open("/home/people/12309511/scripts/auto_gen_tests_pipeline/12_analysis/valid_bugs", "r")
f_bug_struct_report = open("/home/people/12309511/mutation_analysis/bug_struct.csv", "w")

projects = "/home/people/12309511/defects4j/framework/projects"

with f_valid_bugs, f_bug_struct_report:
    report_writer = csv.writer(f_bug_struct_report)

    header = ["Bug-ID", "# Line Additions", "# Line Removals", "# Total Modified Lines"]
    report_writer.writerow(header)

    rows = []

    for line in f_valid_bugs:
        PID = line.split("-")[0]
        VID = line.split("-")[1]
        num = VID.split("f")[0]

        # print(PID, VID, num)

        # PATCH file
        patch = projects + "/" + PID + "/patches/" + num + ".src.patch"
        f_patch = open(patch, "r")

        with f_patch:

            additions = 0
            removals = 0

            for line2 in f_patch:
                if line2.startswith("+ "):
                    additions += 1
                elif line2.startswith("- "):
                    removals += 1

            total_lines = additions + removals
            # print("+:" + str(additions))
            # print("-:" + str(removals))
            # print(total_lines)

            rows.append([PID + "-" + VID, additions, removals, total_lines])

    report_writer.writerows(rows)
