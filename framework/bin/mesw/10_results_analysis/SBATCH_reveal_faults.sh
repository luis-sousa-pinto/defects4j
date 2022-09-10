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

LOG_DIR="/home/people/12309511/logging/12_analysis"

python3 /home/people/12309511/scripts/auto_gen_tests_pipeline/12_analysis/reveal_faults_MAJOR.py $pid $vid || echo "${pid}-${vid}-MAJOR-analysis" >> ${LOG_DIR}/failed_reveal_faults.log
python3 /home/people/12309511/scripts/auto_gen_tests_pipeline/12_analysis/reveal_faults_PIT.py $pid $vid || echo "${pid}-${vid}-PIT-analysis" >> ${LOG_DIR}/failed_reveal_faults.log
