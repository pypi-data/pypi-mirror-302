import xarray as xr
import cfgrib

# This script is intended to be used to convert CARRA data in grib
# format into netcdf format since FALL3D only can read netcdf data.
# However, it could be adapted for other datasets, including ERA5 

### Parameters ###
fname_sfc = 'era5.sfc.20080429-20080429.grib'
fname_lev = 'era5.ml.20080429-20080429.grib'
fname_out = 'merged.grib.ml.nc'
##################

ds_list1 = cfgrib.open_datasets(fname_lev)
ds_list2 = cfgrib.open_datasets(fname_sfc)

keys2remove = ['surface','heightAboveGround']

for ds in ds_list2:
    if 'zust' in ds: ds_list2.remove(ds)

for i,ds in enumerate(ds_list2):
    ds_list2[i] = ds.drop_vars(keys2remove,errors='ignore')
    if 'z' in ds:
        ds_list2[i] = ds.rename_vars({'z': 'z2'})

for ds in ds_list2: print(ds)
ds = xr.merge(ds_list1 + ds_list2)
ds.to_netcdf(fname_out)
