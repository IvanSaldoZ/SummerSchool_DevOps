#!/bin/bash
#
#SBATCH --ntasks=1
#SBATCH --tasks-per-node=1
#SBATCH --time=05:00:00
mpirun -mca btl ^openib /mnt/pool/4/issaldikov/summer_school/mcu01/mcu5/mcu5_free MCU5.INI | tee MCU5.log."$SLURM_JOBID"