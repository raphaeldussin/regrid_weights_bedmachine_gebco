#!/bin/bash
#SBATCH --nodes=7
#SBATCH --job-name="regrid_esmf"
#SBATCH --output=regrid.%j.out
#SBATCH --error=regrid.%j.err
#SBATCH --partition=batch
#SBATCH --clusters=c4
#SBATCH --account=gfdl_o
#SBATCH --qos=urgent
#SBATCH --time=1:00:00

#. /home/Raphael.Dussin/.bashrc

#conda activate repro


time mpirun -np 252 ESMF_RegridWeightGen -s grid_bedmachineAnt.nc -d grid_gebco_southof62.nc -m neareststod -w nearest_weights_srcR.nc --netcdf4 --src_regional

time mpirun -np 252 ESMF_RegridWeightGen -s grid_bedmachineAnt.nc -d grid_gebco_southof62.nc -m bilinear -w bilinear_weights_srcR.nc --netcdf4 --src_regional --ignore_degenerate --ignore_unmapped

tar -cf ESMFlogfiles.tar PET???.RegridWeightGen.Log
rm PET???.RegridWeightGen.Log
