#!/bin/bash

while read -r line; do
	pid=$(echo $line | cut -d"-" -f1)
	vid=$(echo $line | cut -d"-" -f2)
	
	job_name="${pid}-${vid}-analysis-final-run"

	sbatch -J ${job_name} -o /dev/null -e /dev/null SBATCH_reveal_faults.sh $pid $vid

done < valid_bugs
