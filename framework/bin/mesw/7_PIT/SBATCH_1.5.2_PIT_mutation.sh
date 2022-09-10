#!/bin/bash -l

# speficity number of nodes 
#SBATCH -N 1

# specify number of tasks/cores per node required
#SBATCH --ntasks-per-node 1

# specify the walltime e.g 20 mins
#SBATCH -t 144:00:00

# set to email at start,end and failed jobs
#SBATCH --mail-type=NONE
#SBATCH --mail-user=stephen.gaffney@ucdconnect.ie

# run from current directory
cd $SLURM_SUBMIT_DIR

project="$1"
gen="$2"
seed="$3"
version="$4"

log_dir="/home/people/12309511/logging/9_PIT_mut_analysis/${project}"
mkdir --parents $log_dir
suites="/home/people/12309511/test_suites/fixed_suites/${project}/${gen}/${seed}"
out_dir="/home/people/12309511/scratch/pit_mutation_results"
tmp_out="/home/people/12309511/scratch/tmp_out"

# Make tmp dir for checkout etc
tmp_dir="/home/people/12309511/scratch/pit_tmp/${project}-${gen}-${seed}-${version}"
tmp=$(mktemp -d ${tmp_dir}.XXXXXXXXXX)

# Make temporary out directory for mutations.xml file before moving it
out="${tmp_out}/${project}-${gen}-${seed}-${version}"
mkdir --parents $out


# Run PIT
(run_pit.pl -t "${tmp}" -p ${project} -o ${out} -d ${suites} -v ${version}) || echo "${project}-${gen}-${seed}-${version}" >> "${log_dir}/${project}_failed_pit_suites.log"


# If mutations file exists and not empty (PIT worked)
if [ -s "${out}/mutation_log/${project}/${gen}/${version}-${seed}-pitReports/mutations.xml" ]; then

	# Make output directories
	mkdir -p ${out_dir}/${project}/${version}

	# Move matrix
	(mv "${out}/mutation_log/${project}/${gen}/${version}-${seed}-pitReports/mutations.xml" "${out_dir}/${project}/${version}/${version}-${gen}-${seed}-mutations.xml" && echo "${project}-${gen}-${seed}-${version}" >> "${log_dir}/${project}_success_pit_suites.log") || echo "${project}-${gen}-${seed}-${version}" >> "${log_dir}/${project}_not_moved.err"

else
	# No mutation file means error?
	# Avoid duplicates in error file
	if ! grep -Fxq "${project}-${gen}-${seed}-${version}" "${log_dir}/${project}_failed_pit_suites.log"; then
		echo "${project}-${gen}-${seed}-${version}" >> "${log_dir}/${project}_failed_pit_suites.log"
	fi
fi

# Remove temporary dirs
rm -rf "${out}"
rm -rf "${tmp}"
