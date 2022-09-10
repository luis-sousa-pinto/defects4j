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

project="$1"
suite_dir="$2"
gen="$3"
seed="$4"
vid="$5"

out_dir="/home/people/12309511/triggering_tests/${project}/${gen}/${seed}"
mkdir -p ${out_dir}

cmd="run_triggering_test_identification.pl -p ${project} -v ${vid} -d ${suite_dir} -o ${out_dir}/"

eval "$cmd" || echo "$cmd" >> /home/people/12309511/logging/3_run_bug_det_thomas/failed_run_bug_by_vid.log
