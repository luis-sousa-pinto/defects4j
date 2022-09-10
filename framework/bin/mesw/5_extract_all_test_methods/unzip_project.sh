#!/bin/bash

project="$1"
project_dir=/home/people/12309511/test_suites/fixed_suites/${project}
for generator in $project_dir/*; do
	generator_str=$(echo "$generator" | rev | cut -d'/' -f1 | rev)

	for int in $generator/*; do
		int_str=$(echo "$int" | rev | cut -d'/' -f1 | rev)
		mkdir -p /home/people/12309511/scratch/tmp_unzipped/${project}/${generator_str}/${int_str}
		for version in $int/*; do
			if [[ $version == *.tar.bz2 ]]; then
				version_id=$(echo "$version" | cut -f2 -d'-')
				mkdir -p ~/scratch/tmp_unzipped/${project}/${generator_str}/${int_str}/${version_id}
				tar -xvjf "$version" -C ~/scratch/tmp_unzipped/${project}/${generator_str}/${int_str}/${version_id} >> /dev/null 2>> /dev/null
			fi
		done
	done
done

