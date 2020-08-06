#!/usr/bin/env python

import xarray as xr
import numpy as np

#----------------------- bedmachine ---------------------------------
PROJSTRING="+proj=stere +lat_0=-90 +lat_ts=-71 +lon_0=0 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"

def add_lon_lat(ds, PROJSTRING, x='x', y='y', chunks={}):
    """ add longitude and latitude as compute from the inverse projection
    given in PROJSTRING

    PARAMETERS:
    -----------
    ds: xarray.Dataset

    PROJSTRING: str

    """
    from pyproj import CRS, Transformer
    # create the coordinate reference system
    crs = CRS.from_proj4(PROJSTRING)
    # create the projection from lon/lat to x/y
    proj = Transformer.from_crs(crs.geodetic_crs, crs)
    # make x,y 2d arrays
    xx, yy = np.meshgrid(ds[x].values, ds[y].values)
    # compute the lon/lat
    lon, lat = proj.transform(xx, yy, direction='INVERSE')
    # add to dataset
    ds['lon'] = xr.DataArray(data=lon, dims=('y', 'x'))
    ds['lat'] = xr.DataArray(data=lat, dims=('y', 'x'))
    ds['lon'].attrs = dict(units='degrees_east')
    ds['lat'].attrs = dict(units='degrees_north')
    return ds


def create_bedmachine_xy():
    """recreate coordinates from bedmachine into xarray Dataset"""
    x = np.arange(-3333000,3333000+500,500, dtype=np.int32)
    y = np.arange(3333000,-3333000-500,-500, dtype=np.int32)
    ds = xr.Dataset()
    ds['x'] = xr.DataArray(data=x, dims=('x'))
    ds['y'] = xr.DataArray(data=y, dims=('y'))
    ds['x'].attrs = {'long_name': "Cartesian x-coordinate",
                     'standard_name': "projection_x_coordinate",
                     'units': "meter"}
    ds['y'].attrs = {'long_name': "Cartesian y-coordinate",
                     'standard_name': "projection_y_coordinate",
                     'units': "meter"}
    return ds


#----------------------- gebco --------------------------------------

# quite interestingly this function is unable to reproduce bitwise
# identical values from the original gebco grid, with differences O(10e-14)
def create_grid_gebco():
    """ GEBCO has a 30" of arc regular lat/lon grid"""
    increment = np.float64(1) / np.float64(120)
    half = np.float64(1) / np.float64(2)
    nx=360*120
    ny=180*120
    # longitude
    lonmin = np.float64(-180.)
    lonmax = np.float64(180.)
    #lon_center = np.empty((nx), dtype=np.float64)
    #lon_center[0] = lonmin + half * increment
    #for k in range(1,nx):
    #    lon_center[k] = lon_center[0] + (k * increment)
    lon_edges = np.empty((nx+1), dtype=np.float64)
    lon_edges[0] = lonmin
    for k in range(1,nx+1):
        lon_edges[k] = lon_edges[0] + (k * increment)

    lon_center = half * lon_edges[1:] + half * lon_edges[:-1]

    # latitude
    latmin = np.float64(-90.)
    latmax = np.float64(90.)
    lat_center = np.empty((ny), dtype=np.float64)
    lat_center[0] = latmin + half * increment
    for k in range(1,ny):
        lat_center[k] = lat_center[0] + (k * increment)


    ds = xr.Dataset()
    ds['lon'] = xr.DataArray(data=lon_center, dims=('lon'))
    ds['lat'] = xr.DataArray(data=lat_center, dims=('lat'))
    ds['lon'].attrs = {'standard_name': "longitude",
                       'long_name': "longitude",
                       'units': "degrees_east"}
    ds['lat'].attrs = {'standard_name': "latitude",
                       'long_name': "latitude",
                       'units': "degrees_north"}
    return ds


def create_grid_gebco_antarctic(ds):
    """ subset gebco grid where bedmachine exists """
    gebco_SO = gebco.sel(lat=slice(-90, -62))
    gebco_SO['lon'].attrs = dict(units='degrees_east')
    gebco_SO['lat'].attrs = dict(units='degrees_north')
    gebco_encoding = {'lon': {'dtype': 'float64'},
                      'lat': {'dtype': 'float64'}}
    gebco_SO.to_netcdf('grid_gebco_southof62.nc', format='NETCDF3_64BIT',
                       engine='netcdf4', encoding=gebco_encoding)


#----------------------- main ---------------------------------------
if __name__ == '__main__':
    # create gebco grid: not working yet
    #gebco = create_grid_gebco()
    #gebco_encoding = {'lon': {'dtype': 'float64'},
    #                  'lat': {'dtype': 'float64'}}
    #gebco.to_netcdf('grid_gebco_30sec.nc', format='NETCDF3_64BIT',
    #                engine='netcdf4', encoding=gebco_encoding)

    # subset gebco grid:
    gebco = xr.open_dataset('grid_gebco_30sec_original.nc')
    create_grid_gebco_antarctic(gebco)

    # create bedmachine grid:
    bedmachine = create_bedmachine_xy()
    bedmachine = add_lon_lat(bedmachine, PROJSTRING)
    bedmachine_encoding = {'lon': {'dtype': 'float64', '_FillValue': 1.0e+15},
                           'lat': {'dtype': 'float64', '_FillValue': 1.0e+15},
                           'x': {'dtype': 'int32'},
                           'y': {'dtype': 'int32'}}
    bedmachine.to_netcdf('grid_bedmachineAnt.nc', format='NETCDF3_64BIT',
                         engine='netcdf4', encoding=bedmachine_encoding)
