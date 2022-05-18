#!/bin/sh
# https://confluence.columbia.edu/confluence/display/rcs/Habanero+-+Job+Examples#HabaneroJobExamples-PythonandJULIA
#
# Simple "Hello World" submit script for Slurm.
#
#SBATCH --account=free # The account name for the job.
#SBATCH --job-name=count-objects # The job name.
#SBATCH -c 16 # The number of cpu cores to use.
#SBATCH --time=15:00 # The time the job will take to run.
#SBATCH --mem-per-cpu=2gb # The memory the job will use per cpu core.
module load cuda11.2/toolkit cuda11.2/blas cudnn8.1-cuda11.2
module load anaconda
#Command to execute Python program
python3 countObjects-ewiser.py dubliners.txt
#End of script
