import os
import subprocess

log_dir = "/home/people/12309511/logging/9_PIT_mut_analysis"
stats_dir = "/home/people/12309511/logging/10_stats"
pit_dir = "/home/people/12309511/scratch/pit_mutation_results"

# Get overall PIT results

total_success = 0
total_failed = 0

with open(stats_dir + "/PIT_stats", "w") as stats_file:
    stats_file.write("Project\t\tSuccess\tFailures\tPercentage\n")

    for path, dirs, files in os.walk(log_dir):

        for d in dirs:

            project_dir = os.path.join(path, d)
            pid = d

            success_file = project_dir + "/" + pid + "_success_pit_suites.log"
            failed_file = project_dir + "/" + pid + "_failed_pit_suites.log"

            try:
                project_success = int(subprocess.check_output(['wc', '-l', success_file]).split()[0])
            except subprocess.CalledProcessError:
                project_success = 0

            try:
                project_failed = int(subprocess.check_output(['wc', '-l', failed_file]).split()[0])
            except subprocess.CalledProcessError:
                project_failed = 0

            percent = project_success / (project_success + project_failed)
            total_success += project_success
            total_failed += project_failed

            stats_file.write(pid + "\t\t" + str(project_success) + "\t" + str(project_failed) + "\t" + str(percent) + "\n")

    total_percent = total_success / (total_success + total_failed)
    stats_file.write("*" * 50 + "\n")
    stats_file.write("Total" + "\t\t" + str(total_success) + "\t" + str(total_failed) + "\t" + str(total_percent) + "\n")
    stats_file.write("*" * 50 + "\n")

    # Go through PIT results
    bugs_4lt = 0
    bugs_4gte = 0
    bugs_5gte = 0

    f_bugs_4lt = os.path.join(stats_dir, "PIT_bugs_lt4_suites")
    f_bugs_4gte = os.path.join(stats_dir, "PIT_bugs_gte4_suites")
    f_bugs_5gte = os.path.join(stats_dir, "PIT_bugs_gte5_suites")

    with open(f_bugs_4lt, "w") as file_bugs_4lt, open(f_bugs_4gte, "w") as file_bugs_4gte, open(f_bugs_5gte, "w") as file_bugs_5gte:
        for path, dirs, files in os.walk(pit_dir):

            for pid in dirs:
                project_dir = os.path.join(path, pid)

                for path2, dirs2, files2 in os.walk(project_dir):

                    for vid in dirs2:
                        bug_dir = os.path.join(path2, vid)

                        for path3, dirs3, files3 in os.walk(bug_dir):
                            suite_count = 0

                            bug_valid_suites = "/home/people/12309511/logging/10_stats/PIT_bug_valid_suites/" + pid + "-" + vid + "-suites"
                            with open(bug_valid_suites, "w") as suites_file:
                                for file in files3:
                                    suite_count += 1

                                    split = file.split("-")
                                    gen = split[1]
                                    seed = split[2]

                                    suites_file.write(pid + "-" + vid + "-" + gen + "-" + seed + "\n")
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

    file_bugs_4lt.close()
    file_bugs_4gte.close()
    file_bugs_5gte.close()

    stats_file.write("Bugs <4 suites: " + str(bugs_4lt) + "\n")
    stats_file.write("Bugs 4+ suites: " + str(bugs_4gte) + "\n")
    stats_file.write("Bugs 5+ suites: " + str(bugs_5gte) + "\n")

stats_file.close()
