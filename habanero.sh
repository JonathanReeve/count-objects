#!/bin/sh
# https://confluence.columbia.edu/confluence/display/rcs/Habanero+-+Job+Examples#HabaneroJobExamples-PythonandJULIA
#
# Simple "Hello World" submit script for Slurm.
#
#SBATCH --account=free # The account name for the job.
#SBATCH --job-name=count-objects # The job name.
#SBATCH -c 8 # The number of cpu cores to use.
#SBATCH --time=15:00 # The time the job will take to run.
#SBATCH --mem-per-cpu=1gb # The memory the job will use per cpu core.
module load cuda11.2/toolkit cuda11.2/blas cudnn8.1-cuda11.2
module load anaconda
pip install torch torchvision torch-scatter torch-sparse fairseq spacy
git clone https://github.com/pytorch/fairseq
cd fairseq && pip install --editable ./ && cd ..
python -m spacy download en_core_web_trf
git clone https://github.com/SapienzaNLP/ewiser.git
cd ewiser && pip install -r requirements.txt && pip install -e . && cd ..
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"
#Command to execute Python program
python countObjects-ewiser.py dubliners.txt
#End of script
