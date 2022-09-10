#!/bin/bash

projects=(
	Chart
        Cli
        Closure
        Codec
        Collections
        Compress
        Csv
        Gson
        JacksonCore
        JacksonDatabind
        JacksonXml
        Jsoup
        JxPath
        Lang
        Math
        Mockito
        Time
)
# Location of fixed test suites
dir="/home/people/12309511/test_suites/fixed_suites"

log_dir="/home/people/12309511/logging/6_major_mut_analysis"

# Iterate through all fixed test suites
for pid in "${projects[@]}"; do
	project_dir="${dir}/${pid}"

	# Iterate through generators
	for generator in $project_dir/*; do
	        gen=$(echo "$generator" | rev | cut -d'/' -f1 | rev)

		# Iterate through seeds
        	for seed_dir in $generator/*; do
                	seed=$(echo "$seed_dir" | rev | cut -d'/' -f1 | rev)

			# Iterate through versions
			for version in $seed_dir/*; do
       		                if [[ $version == *.tar.bz2 ]]; then

                	                vid=$(echo "$version" | cut -f2 -d'-')
					
					# If vid is in trig tests dir then run mut otherwise don't
					if [ -d /home/people/12309511/triggering_tests/${pid}/${vid} ]; then
						valid_suites_log=${log_dir}/valid_mut_suites.log
						echo ${pid}-${gen}-${seed}-${vid} >> ${valid_suites_log}

						valid_bugs_log=${log_dir}/valid_mut_bugs.log
						
						# If file doesn't exist then create it
						if [ ! -f "$valid_bugs_log" ]; then
					                touch "$valid_bugs_log"
        					fi

						# Avoid duplicate bugs in this file
						if ! grep -Fxq "${pid}-${vid}" "$valid_bugs_log" ; then
							echo ${pid}-${vid} >> "$valid_bugs_log"					
						fi

						# Make directory for logging outputs
						mkdir --parents ${log_dir}/${pid}
						
						job_name=${pid}-${gen}-${seed}-${vid}-major_mutation2
						out_dir=${log_dir}/${pid}

						# Run mut HERE
						sbatch -J ${job_name} -o /dev/null -e ${out_dir}/${job_name}.err SBATCH_mutation2_test_suite.sh $pid $gen $seed $vid
					else
						invalid_suites_log=${log_dir}/invalid_mut_suites.log
						echo ${pid}-${gen}-${seed}-${vid} >> ${invalid_suites_log}

						invalid_bugs_log=${log_dir}/invalid_mut_bugs.log

						# If file doesn't exist then create it
                                                if [ ! -f "$invalid_bugs_log" ]; then
                                                        touch "$invalid_bugs_log"
                                                fi

						if ! grep -Fxq "${pid}-${vid}" "$invalid_bugs_log" ; then
                                                        echo ${pid}-${vid} >> "$invalid_bugs_log"                                  
                                                fi
					fi
				fi
			done
		done
	done
done           
