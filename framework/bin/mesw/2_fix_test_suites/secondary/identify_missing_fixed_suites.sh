#!/bin/bash

raw_suites="/home/people/12309511/test_suites/raw_suites"
fixed_suites="/home/people/12309511/test_suites/fixed_suites"

for project_dir in $raw_suites/*; do
        pid=$(echo "$project_dir" | rev | cut -d'/' -f1 | rev)

        for generator_dir in $project_dir/*; do
                gen=$(echo "$generator_dir" | rev | cut -d'/' -f1 | rev)

                for seed_dir in $generator_dir/*; do
                        seed=$(echo "$seed_dir" | rev | cut -d'/' -f1 | rev)
					
			for file_path in $seed_dir/*; do
				file=$(echo "$file_path" | rev | cut -d'/' -f1 | rev)
				
				fixed_file_path=${fixed_suites}/${pid}/${gen}/${seed}
				
				if [ ! -f ${fixed_file_path}/${file} ]; then
					echo $file >> "/home/people/12309511/logging/2_fix_test_suites/missing_fixed_suites.log"
				fi
			done
		done
	done
done
