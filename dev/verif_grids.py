import xarray as xr
import numpy as np

test_gebco=False
test_bedmachine=True

#gebco
if test_gebco:
    gebco1 = xr.open_dataset('../grid_gebco_30sec.nc')
    gebco2 = xr.open_dataset('../grid_gebco_30sec_original.nc')

    assert np.allclose(gebco1.lon.data, gebco2.lon.data)
    assert np.allclose(gebco1.lat.data, gebco2.lat.data)

    print(np.equal(gebco1.lon.data, gebco2.lon.data)[900:1000])
    print('number of mismatch points in lon array:')
    print(len(np.where(~np.equal(gebco1.lon.data, gebco2.lon.data))[0]))
    print(np.where(~np.equal(gebco1.lon.data, gebco2.lon.data)))
    print(gebco1.lon.data[np.where(~np.equal(gebco1.lon.data, gebco2.lon.data))])

    print('number of mismatch points in lat array:')
    print(len(np.where(~np.equal(gebco1.lat.data, gebco2.lat.data))[0]))

    #print(gebco1.lon.data[:100] - gebco2.lon.data[:100])
    #print(np.equal(gebco1.lat.data, gebco2.lat.data)[:100])
    #print(gebco1.lat.data[:100] - gebco2.lat.data[:100])

    #assert np.equal(gebco1.lon.data, gebco2.lon.data).all()
    #assert np.equal(gebco1.lat.data, gebco2.lat.data).all()
    #assert hash(gebco1.lon.data.tobytes()) == hash(gebco2.lon.data.tobytes())
    #assert hash(gebco1.lat.data.tobytes()) == hash(gebco2.lat.data.tobytes())

#bedmachine
if test_bedmachine:
    bm1 = xr.open_dataset('../grid_bedmachineAnt.nc')
    bm2 = xr.open_dataset('/local2/home/OM4_125_bedmachine_ant1/raw_data/bedmachine+geo.nc')

    assert np.allclose(bm1.lat.data, bm2.lat.data)
    assert np.allclose(bm1.lon.data, bm2.lon.data)
    assert np.allclose(bm1.y.data, bm2.y.data)
    assert np.allclose(bm1.x.data, bm2.x.data)
    assert hash(bm1.lon.data.tobytes()) == hash(bm2.lon.data.tobytes())
    assert hash(bm1.lat.data.tobytes()) == hash(bm2.lat.data.tobytes())
