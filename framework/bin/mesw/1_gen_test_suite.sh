#!/bin/bash -l

# speficity number of nodes 
#SBATCH -N 1

# specify number of tasks/cores per node required
#SBATCH --ntasks-per-node 1

# specify the walltime e.g 20 mins
#SBATCH -t 72:00:00

# set to email at start,end and failed jobs
#SBATCH --mail-type=NONE
#SBATCH --mail-user=stephen.gaffney@ucdconnect.ie

# run from current directory
cd $SLURM_SUBMIT_DIR

generator=$1
project=$2
bug_id=$3
test_id=$4

cmd="gen_tests.pl -g $generator -p $project -v "${bug_id}"f -n $test_id -o $WORKSPACE/generation/test_suites/raw_suites -b 7200"

eval "$cmd" || eval "$cmd" || eval "$cmd" || echo "$cmd" >> $WORKSPACE/generation/logging/1_gen_test_suites/failed_retry_gen_test_suites.log
