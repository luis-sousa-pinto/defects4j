#!/bin/bash -l

# speficity number of nodes 
#SBATCH -N 1

# specify number of tasks/cores per node required
#SBATCH --ntasks-per-node 1

# specify the walltime e.g 20 mins
#SBATCH -t 24:00:00

# set to email at start,end and failed jobs

# run from current directory
cd $SLURM_SUBMIT_DIR

project="$1"

#Unzip project
./unzip_project.sh "$project" || echo "$project" >> /home/people/12309511/logging/5_extract_all_test_methods/unzip_failed.log

#Call the copy test script
./copy_test_methods.sh "$project" || echo "$project" >> /home/people/12309511/logging/5_extract_all_test_methods/copy_test_methods_failed.log

#Delete the project dir when tests are retrieved
rm -rf /home/people/12309511/scratch/tmp_unzipped/${project}
