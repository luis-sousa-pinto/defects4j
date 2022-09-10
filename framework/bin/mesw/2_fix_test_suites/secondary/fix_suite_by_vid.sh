#!/bin/bash

log_dir=/home/people/12309511/logging/2_fix_test_suites

while read -r line || [[ -n $line ]]; do

	if [[ $line == "perl "* ]]; then
		pid=$(echo $line | cut -d" " -f4)
		suite_dir=$(echo $line | cut -d" " -f6)

		gen=$(echo $suite_dir | cut -d"/" -f8)
		seed=$(echo $suite_dir | cut -d"/" -f9)

		for file in $suite_dir/*; do
			if [[ $file == *".tar.bz2" ]]; then
				filename=$(echo $file | rev | cut -d"/" -f1 | rev)
				vid=$(echo $filename | cut -d"-" -f2)
				
				version_log_dir=${log_dir}/${pid}/${gen}-${seed}
				version_error_file=${version_log_dir}/${vid}.error
				mkdir -p "${version_log_dir}"

				job_name=${pid}_${vid}_${gen}_${seed}_fix
				
				#sbatch -J ${job_name} -o "/home/people/12309511/scratch/dump.out" -e ${version_error_file} SBATCH_fix_suite_by_vid.sh $pid $vid $suite_dir
				sbatch -J ${job_name} -o "/dev/null" -e ${version_error_file} SBATCH_fix_suite_by_vid.sh $pid $vid $suite_dir
			fi
		done

	fi

done < ${log_dir}/failed_fix_suites.log
