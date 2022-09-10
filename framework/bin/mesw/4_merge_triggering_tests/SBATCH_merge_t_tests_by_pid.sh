#!/bin/bash -l

# speficity number of nodes 
#SBATCH -N 1

# specify number of tasks/cores per node required
#SBATCH --ntasks-per-node 1

# specify the walltime e.g 20 mins
#SBATCH -t 48:00:00

# set to email at start,end and failed jobs
#SBATCH --mail-type=NONE
#SBATCH --mail-user=stephen.gaffney@ucdconnect.ie

# run from current directory
cd $SLURM_SUBMIT_DIR


read_properties_file() {
	pid=$1
	vid=$2
	gen=$3
	seed=$4
	file=$5

	#Read each line in file, if matches format then extract test method and append IDS

	# Remove target tests part
	tests=$(cat $file | cut -d" " -f3)
		
	# Multiple deliminted test names
	if [[ $tests == *";"* ]]; then
		make_trig_test_folder $pid $vid $gen $seed
		i=1
		while :; do
			test_name=$(echo $tests | cut -d";" -f"$i" | cut -d"(" -f1)
			
			# Break out at EOF
			if [[ $test_name == "" ]]; then
				break
			fi

			# Try write test to file
			write_test_to_file $pid $vid $gen $seed $test_name
			i=$((i+1))
		done

	# Single test in properties file
	else
		make_trig_test_folder $pid $vid $gen $seed
		test_name=$(echo $tests | cut -d"(" -f1)

		write_test_to_file $pid $vid $gen $seed $test_name
	fi
}

make_trig_test_folder() {
	pid=$1
	vid=$2
	gen=$3
	seed=$4

	mkdir --parents "/home/people/12309511/triggering_tests/${pid}/${vid}"
}

write_test_to_file() {
	pid=$1
        vid=$2
        gen=$3
        seed=$4
	test_name=$5

	vid_test_name="${vid}-${gen}-${seed}-${test_name}"
	file_location="/home/people/12309511/triggering_tests/${pid}/${vid}/${pid}-${vid}-triggering_tests"	
	
	# If file doesn't exist then create it
	if [ ! -f "$file_location" ]; then
		touch "$file_location"
	fi
	
	# Append test to file if not already present (Prevents duplicates)
	if ! grep -Fxq "$vid_test_name" "$file_location" ; then
        	echo "$vid_test_name" >> "$file_location"
	else
        	echo "${pid}_${vid_test_name}" >> /home/people/12309511/logging/4_merge_triggering_tests/${pid}_duplicated_test_names.log
	fi
}

pid=$1

# Location of all triggering tests
t_tests_dir="/home/people/12309511/triggering_tests"
proj_dir=${t_tests_dir}/${pid}

for gen_dir in $proj_dir/*; do
	gen_str=$(echo "$gen_dir" | rev | cut -d'/' -f1 | rev)

	if [ "$gen_str" = "evosuite" ] || [ "$gen_str" = "randoop" ]; then
	#if [ "$gen_str" = "evosuite" ]; then

		for seed_dir in $gen_dir/*; do
			seed=$(echo "$seed_dir" | rev | cut -d'/' -f1 | rev)

			for file_path in $seed_dir/*; do
				file=$(echo "$file_path" | rev | cut -d'/' -f1 | rev)

				if [[ $file == ${pid}-*-*.properties ]]; then
					#echo "Working on file-" $file
					
					vid=$(echo $file | cut -d'-' -f2)	
					read_properties_file $pid $vid $gen_str $seed $file_path
				fi
			done
		done
	fi
done

