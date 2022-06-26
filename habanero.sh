#!/bin/sh
# https://confluence.columbia.edu/confluence/display/rcs/Habanero+-+Job+Examples#HabaneroJobExamples-PythonandJULIA
#
# Simple "Hello World" submit script for Slurm.
#
#SBATCH --account=free # The account name for the job.
#SBATCH --job-name=count-objects # The job name.
#SBATCH -c 24 # The number of cpu cores to use.
#SBATCH --time=0-08:00:00 # The time the job will take to run.
#SBATCH --constraint=p100 --gres=gpu
#SBATCH --mem-per-cpu=4gb # The memory the job will use per cpu core.
module load cuda11.2/toolkit cuda11.2/blas cudnn8.1-cuda11.2
module load anaconda
#Command to execute Python program
python3 countObjects-annotate.py corpus-pg-3
#End of script
