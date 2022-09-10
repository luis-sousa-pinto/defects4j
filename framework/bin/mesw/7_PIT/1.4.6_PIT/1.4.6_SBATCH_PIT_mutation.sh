#!/bin/bash -l

# speficity number of nodes 
#SBATCH -N 1

# specify number of tasks/cores per node required
#SBATCH --ntasks-per-node 1

# specify the walltime e.g 20 mins
#SBATCH -t 120:00:00

# set to email at start,end and failed jobs
#SBATCH --mail-type=NONE
#SBATCH --mail-user=stephen.gaffney@ucdconnect.ie

# run from current directory
cd $SLURM_SUBMIT_DIR

project="$1"
gen="$2"
seed="$3"
version="$4"

log_dir="/home/people/12309511/logging/1.4.6_pit_logging"
suites="/home/people/12309511/test_suites/fixed_suites/${project}/${gen}/${seed}"
out_dir="/home/people/12309511/scratch/1.4.6_pit_results"
tmp_out="/home/people/12309511/scratch/tmp_out2"

# Make temporary out directory for mutations.xml file before moving it
out="${tmp_out}/${project}-${gen}-${seed}-${version}"
mkdir --parents $out

# Run PIT
(run_pit.pl -p ${project} -o ${out} -d ${suites} -v ${version}) || echo "${project}-${version}-${gen}-${seed}" >> "${log_dir}/failed_pit_suites.log"

# If mutations file exists (PIT worked)
if [ -f "${out}/mutation_log/${project}/${gen}/${version}-${seed}-pitReports/mutations.xml" ]; then

	# Make output directories
	mkdir -p ${out_dir}/${project}/${version}

	# Move matrix
	(mv "${out}/mutation_log/${project}/${gen}/${version}-${seed}-pitReports/mutations.xml" "${out_dir}/${project}/${version}/${version}-${gen}-${seed}-mutations.xml" && echo "${project}-${version}-${gen}-${seed}" >> "${log_dir}/success_pit_suites.log") || echo "${project}-${version}-${gen}-${seed}" >> "${log_dir}/not_moved.err"

else
	# No mutation file means error?
	# Avoid duplicates in error file
	if ! grep -Fxq "${project}-${version}-${gen}-${seed}" "${log_dir}/failed_pit_suites.log"; then
		echo "${project}-${version}-${gen}-${seed}" >> "${log_dir}/failed_pit_suites.log"
	fi
fi

# Remove temporary checkout
rm -rf "${out}"
