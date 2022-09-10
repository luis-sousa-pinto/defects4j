#!/bin/bash

while read -r line; do
	pid=$(echo $line | cut -d"-" -f1)
	vid=$(echo $line | cut -d"-" -f2)
	
	job_name="${pid}-${vid}-merge_common_suites_MAJOR_python"

	sbatch -J ${job_name} -o /dev/null -e /dev/null SBATCH_MAJOR_merge.sh $pid $vid
	
	cp "/home/people/12309511/scratch/major_mutation_results/${pid}/${vid}/mutants.log" "/home/people/12309511/scratch/MAJOR_valid_maps/${pid}/${vid}/${pid}-${vid}-mutants.log" || echo ${pid}-${vid} >> failed_copy.log

done < merge_common_bugs
