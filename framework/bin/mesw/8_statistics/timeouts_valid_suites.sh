#!/bin/bash

major="/home/people/12309511/scratch/major_mutation_results"
valid_suites="/home/people/12309511/logging/10_stats/MAJOR_bug_valid_suites"

total=0
total_suites=0

while read -r line<&3; do
	pid=$(echo $line | cut -d"-" -f1)
	vid=$(echo $line | cut -d"-" -f2)

	echo $pid $vid
	
	maps_dir="${major}/${pid}/${vid}/kill_maps"
	
	count=$(ls ${maps_dir} | cut -d"-" -f2-3 | uniq | wc -l)
	ls ${maps_dir} | cut -d"-" -f2-3 | uniq | while read -r output; do
		echo $pid-$vid-$output >> "${valid_suites}/${pid}-${vid}-suites"
	done

	if (( count >= 5 )); then
		total=$((total + 1))
		total_suites=$((total_suites + count))
	fi
done 3< TIMEOUT_10_day.log

echo "Total bugs:" $total
