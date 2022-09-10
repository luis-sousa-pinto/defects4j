import os

maps_dir = "/home/people/12309511/scratch/merged_major_maps"
stats_dir = "/home/people/12309511/logging/10_stats"

# Go through Major results
bugs_4lt = 0
bugs_4gte = 0
bugs_5gte = 0

f_bugs_4lt = os.path.join(stats_dir, "MAJOR_bugs_lt4_suites")
f_bugs_4gte = os.path.join(stats_dir, "MAJOR_bugs_gte4_suites")
f_bugs_5gte = os.path.join(stats_dir, "MAJOR_bugs_gte5_suites")

with open(f_bugs_4lt, "w") as file_bugs_4lt, open(f_bugs_4gte, "w") as file_bugs_4gte, open(f_bugs_5gte, "w") as file_bugs_5gte, open(stats_dir + "/MAJOR_stats", "w") as stats_file:
    for path, dirs, files in os.walk(maps_dir):

        for pid in dirs:
            project_dir = os.path.join(path, pid)

            for path2, dirs2, files2 in os.walk(project_dir):

                for vid in dirs2:
                    bug_dir = os.path.join(path2, vid)
                    bug_map = bug_dir + "/" + pid + "-" + vid + "-mergedMap.csv"

                    suite_count = 0

                    bug_valid_suites = "/home/people/12309511/logging/10_stats/MAJOR_bug_valid_suites/" + pid + "-" + vid + "-suites"

                    with open(bug_valid_suites, "w") as suites_file:
                        for gen in ["evosuite", "randoop"]:
                            for seed in range(1, 6, 1):
                                pattern = gen + "-" + str(seed)

                                with open(bug_map, "r") as map_read:

                                    if pattern in map_read.read():
                                        suite_count += 1

                                        # Write to file here
                                        suites_file.write(pid + "-" + vid + "-" + gen + "-" + str(seed) + "\n")

                                        continue

                                map_read.close()

                        # Check for dev suite
                        with open(bug_map, "r") as map_read:

                            if "-dev-dev-" in map_read.read():
                                suite_count += 1

                                # Write to file here
                                suites_file.write(pid + "-" + vid + "-dev-dev\n")

                        map_read.close()
                    suites_file.close()

                    if suite_count < 4:
                        bugs_4lt += 1
                        file_bugs_4lt.write(pid + "-" + vid + "\n")
                    if suite_count >= 4:
                        bugs_4gte += 1
                        file_bugs_4gte.write(pid + "-" + vid + "\n")
                    if suite_count >= 5:
                        bugs_5gte += 1
                        file_bugs_5gte.write(pid + "-" + vid + "\n")

    stats_file.write("Bugs <4 suites: " + str(bugs_4lt) + "\n")
    stats_file.write("Bugs 4+ suites: " + str(bugs_4gte) + "\n")
    stats_file.write("Bugs 5+ suites: " + str(bugs_5gte) + "\n")

file_bugs_4lt.close()
file_bugs_4gte.close()
file_bugs_5gte.close()
stats_file.close()
