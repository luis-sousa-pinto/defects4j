#!/bin/bash -l

# speficity number of nodes
#SBATCH -N 1

# specify number of tasks/cores per node required
#SBATCH --ntasks-per-node 1

# specify the walltime e.g 20 mins
#SBATCH -t 240:00:00

# set to email at start,end and failed jobs
#SBATCH --mail-type=NONE
#SBATCH --mail-user=stephen.gaffney@ucdconnect.ie

# run from current directory
cd $SLURM_SUBMIT_DIR

# Pass project and bug id
pid=$1
vid=$2

out_dir="/home/people/12309511/scratch/PIT_valid_maps/${pid}/${vid}"
log_dir="/home/people/12309511/logging/11_merge_maps"

mkdir -p "${out_dir}"

# Setup master file and remove existing file
master="${out_dir}/${pid}-${vid}-PITmerged.csv"
rm -f "${master}"

# Call python script
(python3 "/home/people/12309511/scripts/auto_gen_tests_pipeline/11_merge_maps/PIT/PIT_merge.py" "$pid" "$vid" && echo "${pid}-${vid}" >> "${log_dir}/success_merge.log") || echo "${pid}-${vid}" >> "${log_dir}/failed_merge.log"

