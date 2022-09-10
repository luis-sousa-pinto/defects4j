#!/bin/bash

# Location of fixed test suites
dir="/home/people/12309511/test_suites/fixed_suites"

log_dir="/home/people/12309511/logging/6_major_mut_analysis/timed_out_redo"

mkdir --parents $log_dir

while read -r line; do

        if [ -n "$line" ] && [[ $line == *"TIMEOUT"* ]]; then
                
                f1=$(echo $line | cut -d" " -f1)
                pid=$(echo $f1 | cut -d"-" -f1)
                gen=$(echo $f1 | cut -d"-" -f2)
                seed=$(echo $f1 | cut -d"-" -f3)
                vid=$(echo $f1 | cut -d"-" -f4)

		#Make directory for logging outputs
                mkdir --parents ${log_dir}/${pid}

		job_name=${pid}-${gen}-${seed}-${vid}-major_mutation2_time_outs
		out_dir=${log_dir}/${pid}

                # Run mut HERE
                sbatch -J ${job_name} -o /dev/null -e ${out_dir}/${job_name}.err SBATCH_mutation2_timed_outs.sh $pid $gen $seed $vid
                
        fi
done < timed_out_Chart_suites.log

