#!/bin/bash

major="/home/people/12309511/logging/10_stats/MAJOR_bug_valid_suites"
pit="/home/people/12309511/logging/10_stats/PIT_bug_valid_suites"
dir5="/home/people/12309511/logging/10_stats/5gte_suite_bugs"
dir4="/home/people/12309511/logging/10_stats/4gte_suite_bugs"

total=0
total_suites=0

for file_path in $major/*; do
	file=$(echo $file_path | rev | cut -d"/" -f1 | rev)
	pid=$(echo $file | cut -d"-" -f1)
	vid=$(echo $file | cut -d"-" -f2)

	other_path="${pit}/${file}"

	if [ -s "${other_path}" ]; then
		
		output=$(grep -Fxf ${file_path} ${other_path})
		count=$(echo "${output}" | wc -l)
	
		if (( count >= 5 )); then
			echo "${output}" > "${dir5}/${pid}-${vid}-suites"
			#total=$((total+1))
			#total_suites=$((total_suites + count))
		fi

		if (( count >= 4 )); then
                        echo "${output}" > "${dir4}/${pid}-${vid}-suites"
			total=$((total+1))
                        total_suites=$((total_suites + count))
                fi

	fi
done

echo "Total bugs:" $total

echo "Total suites:" $total_suites
