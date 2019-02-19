#!/bin/bash
#SBATCH --array=00-18%1
#SBATCH --requeue
#SBATCH --partition=staging
#SBATCH --time=48:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=j.p.m.aerts@tudelft.nl

module load python
python api_era5_2m_temperature.py ${SLURM_ARRAY_TASK_ID}