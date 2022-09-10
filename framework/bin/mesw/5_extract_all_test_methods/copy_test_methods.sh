#!/bin/bash

find_java_files_recur () {
	dir=$1
	for file in $dir/*; do
		if [ -d "$file" ]; then
			find_java_files_recur "$file" $2 $3 $4 $5
		else
			check_file_type "$file" $2 $3 $4 $5
		fi
	done
}

check_file_type () {
	file=$1
	
	if [[ ${file} != *"scaffolding.java"* ]] && [[ ${file} = *".java" ]]; then
		search_for_tests "$file" $2 $3 $4 $5
	fi
}

search_for_tests () {
	file=$1
	generator=$3

	package=""

	echo "$file"
	echo "$generator"

	if [ "$generator" = "evosuite" ]; then
		package=$(grep "$file" -e "package" | cut -d " " -f2)
		package=$(echo "${package//;}")
		package="${package}."
		echo $package 	
	fi

	grep "$file" -e "public" | while read -r line; do
		result=$( echo "$line" | cut -d" " -f3)
		if [ -n "$result" ] && [[ $result == *"Test"* ]]; then
			echo "${package}${result}" >> /home/people/12309511/all_test_methods/${project}/${generator_str}/${int_str}/${version_str}/test_methods.txt 
		elif [ -n "$result" ] && [[ $result == *"test"* ]]; then
			echo "${result}" >> /home/people/12309511/all_test_methods/${project}/${generator_str}/${int_str}/${version_str}/test_methods.txt
		fi
	done
}

project="$1"
project_dir=/home/people/12309511/scratch/tmp_unzipped/${project}
for generator in $project_dir/*; do
        generator_str=$(echo "$generator" | rev | cut -d'/' -f1 | rev)
        for int in $generator/*; do
                int_str=$(echo "$int" | rev | cut -d'/' -f1 | rev)
                mkdir -p /home/people/12309511/all_test_methods/${project}/${generator_str}/${int_str}/
                for version in $int/*; do
			version_str=$(echo "$version" | rev | cut -d'/' -f1 | rev) 
			mkdir -p /home/people/12309511/all_test_methods/${project}/${generator_str}/${int_str}/${version_str}
			find_java_files_recur "$version" "$project" "$generator_str" "$int_str" "$version_str"
		done
	done
done
