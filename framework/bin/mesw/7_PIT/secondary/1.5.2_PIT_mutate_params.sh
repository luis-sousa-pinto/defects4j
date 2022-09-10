#!/bin/bash

pid=$1
gen=$2
seed=$3

# Location of fixed test suites
dir="/home/people/12309511/test_suites/fixed_suites/${pid}/${gen}/${seed}"


log_dir="/home/people/12309511/logging/9_PIT_mut_analysis/${pid}"
mkdir --parents $log_dir
tmp_log_dir="/home/people/12309511/scratch/tmp_logging/9_PIT_mut_analysis/${pid}"
mkdir --parents $tmp_log_dir

# Iterate through versions
for version in $dir/*; do
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

                        job_name="${pid}-${gen}-${seed}-${vid}-PIT-split-mutation-1.5.2"

                        # Run mut HERE
                        sbatch -J ${job_name} -o /dev/null -e ${tmp_log_dir}/${job_name}.out SBATCH_1.5.2_PIT_mutation.sh $pid $gen $seed $vid
                 else			
			# Vid is not in trig test dir

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
