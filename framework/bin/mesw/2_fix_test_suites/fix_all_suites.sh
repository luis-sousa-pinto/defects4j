#!/bin/bash

suites="/home/people/12309511/test_suites/fixed_suites"

for project_dir in $suites/*; do
	pid=$(echo "$project_dir" | rev | cut -d'/' -f1 | rev)

	#proj_log_dir=/home/people/12309511/logging/2_fix_test_suites/${pid}
	#mkdir -p "${proj_log_dir}"

	for generator_dir in $project_dir/*; do
		gen=$(echo "$generator_dir" | rev | cut -d'/' -f1 | rev)

              	for seed_dir in $generator_dir/*; do
			seed=$(echo "$seed_dir" | rev | cut -d'/' -f1 | rev)

			job_name=${pid}_${gen}_${seed}
			#sbatch -J ${job_name}_fix -o /dev/null -e "${proj_log_dir}/${job_name}.error" SBATCH_fix_test_suites.sh "$pid" "$seed_dir"
			sbatch -J ${job_name}_fix -o /dev/null -e /dev/null SBATCH_fix_test_suites.sh "$pid" "$seed_dir"
                                
                done
        done
done
