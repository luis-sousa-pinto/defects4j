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

pid=$1
suite_dir=$2

cmd="perl /home/people/12309511/defects4j/framework/util/fix_test_suite.pl -p $pid -d $suite_dir -A"

eval "$cmd" || echo "$cmd" >> /home/people/12309511/logging/2_fix_test_suites/failed_fix_suites.log
