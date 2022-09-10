#!/bin/bash

log_dir=/home/people/12309511/logging/3_run_bug_det_thomas

proj_log_dir=/home/people/12309511/logging/3_run_bug_det_thomas/run_by_vid
mkdir -p ${proj_log_dir}

while read -r line || [[ -n $line ]]; do
	pid=$(echo $line | cut -d' ' -f3)
	suite_dir=$(echo $line | cut -d' ' -f5)
	gen=$(echo $line | cut -d' ' -f5 | cut -d'/' -f8)
	seed=$(echo $line | cut -d' ' -f5 | cut -d'/' -f9)

	for file in $suite_dir/*; do
		
		if [[ $file == *".tar.bz2" ]]; then
			filename=$(echo $file | rev | cut -d"/" -f1 | rev)
			vid=$(echo $filename | cut -d"-" -f2)

			job_name=${pid}_${gen}_${seed}_${vid}
			sbatch -J ${job_name}_run_bug_det -o /dev/null -e "${proj_log_dir}/${job_name}.error" SBATCH_run_bug_det_thomas_by_vid.sh "$pid" "$suite_dir" "$gen" "$seed" "$vid"

		fi
	done
done < ${log_dir}/failed_run_bug.log
