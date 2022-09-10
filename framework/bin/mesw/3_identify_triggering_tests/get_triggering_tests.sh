#!/bin/bash

suite_dir="/home/people/12309511/test_suites/fixed_suites"

for proj_dir in $suite_dir/*; do
	pid=$(echo "$proj_dir" | rev | cut -d'/' -f1 | rev)

	proj_log_dir=/home/people/12309511/logging/3_run_bug_det_thomas/${pid}
	mkdir -p ${proj_log_dir}
	
	for gen_dir in $proj_dir/*; do
		gen=$(echo "$gen_dir" | rev | cut -d'/' -f1 | rev)
              
		for seed_dir in $gen_dir/*; do
			seed=$(echo "$seed_dir" | rev | cut -d'/' -f1 | rev)
                               				
			#sbatch
			job_name=${pid}_${gen}_${seed}

                        sbatch -J ${job_name}_trigs -o /dev/null -e "${proj_log_dir}/${job_name}.error" SBATCH_run_bug_det_thomas.sh "$pid" "$seed_dir" "$gen" "$seed"
                done
        done
done
