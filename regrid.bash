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

# NB: the mpirun used here is the one coming from recompiling mpi4py with gcc on gaea
# see .gitlab-cici.yml for directions

time mpirun -np 252 ESMF_RegridWeightGen -s grid_bedmachineAnt.nc -d grid_gebco_30sec_southof62.nc -m neareststod -w nn_weights_bedmachine_gebco30sec.nc --netcdf4 --src_regional

time mpirun -np 252 ESMF_RegridWeightGen -s grid_bedmachineAnt.nc -d grid_gebco_15sec_southof62.nc -m neareststod -w nn_weights_bedmachine_gebco15sec.nc --netcdf4 --src_regional

# one could get bilinear weights using:

#time mpirun -np 252 ESMF_RegridWeightGen -s grid_bedmachineAnt.nc -d grid_gebco_30sec_southof62.nc -m bilinear -w bilin_weights_bedmachine_gebco30sec.nc --netcdf4 --src_regional --ignore_degenerate --ignore_unmapped

#time mpirun -np 252 ESMF_RegridWeightGen -s grid_bedmachineAnt.nc -d grid_gebco_15sec_southof62.nc -m bilinear -w bilin_weights_bedmachine_gebco15sec.nc --netcdf4 --src_regional --ignore_degenerate --ignore_unmapped

tar -cf ESMFlogfiles.tar PET???.RegridWeightGen.Log
rm PET???.RegridWeightGen.Log
