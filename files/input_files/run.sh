#!/bin/bash
#
#PBS -q short
#PBS -l nodes=1:ppn=1,walltime=00:15:00
cp /mnt/pool/1/dep_573_tmp28/mcu/MCU5.INI /mnt/pool/1/issaldikov/summer_school/mcu28/
cd /mnt/pool/1/issaldikov/summer_school/mcu28/
mpirun ./mcu5/mcu5_free 1>/mnt/pool/1/dep_573_tmp28/mcu/out.txt 2>/mnt/pool/1/dep_573_tmp28/mcu/err.txt
