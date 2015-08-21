#!/bin/bash
#$ -V               # preserve environment variables
#$ -S /bin/bash     # specify which shell to use
#$ -cwd             # cd to current folder before executing the script

#$ -o /home/ucgbpgl/git/testtune/logall    # redirect standard output
#$ -e /home/ucgbpgl/git/testtune/logall    # redirect standard error
#$ -j y

#$ -l tmem=8G       # max memory limit
#$ -l h_vmem=8G     # max memory limit
#$ -l h_rt=03:00:00 # max runtime
#$ -l h_stack=1G    # hard limit on max stack size (SGE sets this to 'unlimited' by default and this can cause some applications to crash)

#$ -N  Allen

##======END OF SGE OPTIONS===========


echo "Starting..."

python tuneAllen.py -nogui

echo "Done!"
