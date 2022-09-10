#!/bin/bash -l

# speficity number of nodes 
#SBATCH -N 1

# specify number of tasks/cores per node required
#SBATCH --ntasks-per-node 1

# specify the walltime e.g 20 mins
#SBATCH -t 192:00:00

# set to email at start,end and failed jobs
#SBATCH --mail-type=NONE
#SBATCH --mail-user=stephen.gaffney@ucdconnect.ie

# run from current directory
cd $SLURM_SUBMIT_DIR

project="$1"
gen="$2"
seed="$3"
version="$4"

# Checkout project version temporarly to scratch space
tmp_dir=/home/people/12309511/scratch/redo_checkouts

mkdir --parents $tmp_dir
defects4j checkout -p $project -v $version -w "${tmp_dir}/${project}_${version}_${gen}_${seed}"

# Switch to checkout as working directory
cd "${tmp_dir}/${project}_${version}_${gen}_${seed}"

# Compile project
defects4j compile

# Run d4j mutation2
(defects4j mutation2 -t testClass::testMethod -s /home/people/12309511/test_suites/fixed_suites/$project/$gen/$seed/${project}-${version}-${gen}.${seed}.tar.bz2 && echo "${project}-${version}-${gen}.${seed}.tar.bz2" >> /home/people/12309511/logging/6_major_mut_analysis/redo_timed_out_CHART_success_mut_suites.log) || echo "${project}-${version}-${gen}.${seed}.tar.bz2" >> /home/people/12309511/logging/6_major_mut_analysis/redo_timed_out_CHART_failed_mut_suites.log

# Remove temporary checkout
rm -rf "${tmp_dir}/${project}_${version}_${gen}_${seed}"
