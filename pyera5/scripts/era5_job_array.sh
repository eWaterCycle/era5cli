#!/bin/bash
#SBATCH --array=00-18%1
#SBATCH --requeue
#SBATCH --partition=staging
#SBATCH --time=30:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=j.p.m.aerts@tudelft.nl

module load python
python api_era5_download.py ${SLURM_ARRAY_TASK_ID} total_precipitation
python api_era5_download.py ${SLURM_ARRAY_TASK_ID} precipitation_type
python api_era5_download.py ${SLURM_ARRAY_TASK_ID} 10m_u_component_of_wind
python api_era5_download.py ${SLURM_ARRAY_TASK_ID} 10m_v_component_of_wind
python api_era5_download.py ${SLURM_ARRAY_TASK_ID} 2m_temperature
python api_era5_download.py ${SLURM_ARRAY_TASK_ID} skin_temperature
python api_era5_download.py ${SLURM_ARRAY_TASK_ID} 2m_dewpoint_temperature
python api_era5_download.py ${SLURM_ARRAY_TASK_ID} volumetric_soil_water_layer_1
python api_era5_download.py ${SLURM_ARRAY_TASK_ID} potential_evaporation
python api_era5_download.py ${SLURM_ARRAY_TASK_ID} evaporation
python api_era5_download.py ${SLURM_ARRAY_TASK_ID} surface_net_solar_radiation
python api_era5_download.py ${SLURM_ARRAY_TASK_ID} temperature_of_snow_layer
python api_era5_download.py ${SLURM_ARRAY_TASK_ID} snowfall
python api_era5_download.py ${SLURM_ARRAY_TASK_ID} runoff