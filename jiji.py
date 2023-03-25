import netCDF4 as nc
import numpy as np

file = '/Users/leo/Desktop/MarineTechTest9_EINino_LaNina/Data/Jason3/cycle215/JA3_OPR_2PfS215_015_20211209_231527_20211210_011145.nc'
dataset = nc.Dataset(file)
print(dataset)
lat = np.array(dataset.variables['lat'][:])
lon = np.array(dataset.variables['lon'][:])
ssha = np.array(dataset.variables['ssha'][:])
print(lat, lon, ssha, sep='\n')
print(lat.shape, lon.shape, ssha.shape)
