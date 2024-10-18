from metpy.units import units
import xarray as xr
import metpy.calc as mpcalc
import numpy as np
import os
from scipy.ndimage import gaussian_filter
from pathlib import Path
from metpy.units import units


def calculate_theta_w(ta, hus, p):
    ta = ta * units.kelvin
    hus = hus * units.dimensionless
    p = p * units.hPa
    
    dp = mpcalc.dewpoint_from_specific_humidity(p, ta, hus)    
    theta_w = mpcalc.wet_bulb_potential_temperature(p, ta, dp)
    
    return theta_w

def gaussian_smoothing(data, sigma=1):
    return gaussian_filter(data, sigma=sigma)


def calculate_tfp(dthdx, dthdy, lons, lats):
    dx, dy = mpcalc.lat_lon_grid_deltas(lons, lats)

    mag_dth = np.sqrt(dthdx**2 + dthdy**2)
    dthdx2 = dthdx / mag_dth
    dthdy2 = dthdy / mag_dth

    dthdx_mag = np.empty_like(mag_dth) * units("kelvin/meter**2")
    dthdy_mag = np.empty_like(mag_dth) * units("kelvin/meter**2")
    
    for i in range(mag_dth.shape[0]):
        dthdx_mag[i, :, :], dthdy_mag[i, :, :] = mpcalc.gradient(mag_dth[i, :, :], axes=[-1, -2], deltas=(dx, dy))

    
    tfp = -1 * (dthdx_mag * dthdx2 + dthdy_mag * dthdy2)

    tfp = tfp*1e8 # Convert to Kelvin/100km²
    mag_dth = mag_dth*1e5 # Convert to Kelvin/100km

    return tfp, mag_dth

def calculate_vf(u, v, tfp, lons, lats):
    dx, dy = mpcalc.lat_lon_grid_deltas(lons, lats)
    dtfpdx = np.empty_like(tfp)
    dtfpdy = np.empty_like(tfp)
    for i in range(tfp.shape[0]):
        dtfpdx[i, :, :], dtfpdy[i, :, :] = mpcalc.gradient(tfp[i, :, :], axes=[-1, -2], deltas=(dx, dy))

    mag_dtfp = np.sqrt(dtfpdx**2 + dtfpdy**2)
    
    vf = (u * dtfpdx / mag_dtfp) + (v * (dtfpdy / mag_dtfp))
    vf = vf * units("m/s")
    return vf

def save_to_netcdf(filepath, lons, lats, time, tfp, mag_dth, vf):
    ds = xr.Dataset(
        {
            'tfp': (('time', 'lat', 'lon'), tfp.data),
            'mag_thetaw': (('time', 'lat', 'lon'), mag_dth.data),
            'vf': (('time', 'lat', 'lon'), vf.data),
        },
        coords={
            'lon': lons,
            'lat': lats,
            'time': time
        }
    )
    
    ds.to_netcdf(filepath)
    print(f'Data saved in: {filepath}')

def process_tfp(ds, start_date, end_date, model_name, output_directory_fronts, pressure=850, smooth_sigma=0.5):   
    if model_name is None:
        model_name = "MyData"
    if 'longitude' in ds.coords:
        ds = ds.rename({"longitude": "lon"})
    if 'latitude' in ds.coords:
        ds = ds.rename({"latitude": "lat"})

    ds = ds.sel(time=slice(start_date,end_date))

    variable_names = {
        'ta': ['t', 'ta', 'temperature', 'air_temperature'], 
        'hus': ['q', 'hus', 'specific_humidity', 'humidity'], 
        'u': ['ua', 'u_component', 'u', 'u-component_of_wind_isobaric'], 
        'v': ['va', 'v_component', 'v', 'v-component_of_wind_isobaric'] 
    }

    def find_variable(ds, var_name_list):
        for name in var_name_list:
            if name in ds:
                return ds[name]
        raise ValueError(f"None of the variables {var_name_list} found in dataset.")
    
    ta = find_variable(ds, variable_names['ta'])
    hus = find_variable(ds, variable_names['hus'])
    u = find_variable(ds, variable_names['u'])
    v = find_variable(ds, variable_names['v'])
    
    lons = ds.lon.values * units.degrees
    lats = ds.lat.values * units.degrees
    dx, dy = mpcalc.lat_lon_grid_deltas(lons, lats)
    
    theta_w = calculate_theta_w(ta, hus, pressure)
    theta_w_smooth = gaussian_smoothing(theta_w, sigma=smooth_sigma)  * units.kelvin

    dthdx = np.empty_like(theta_w_smooth) * units("kelvin/meter")
    dthdy = np.empty_like(theta_w_smooth) * units("kelvin/meter")

    for i in range(theta_w_smooth.shape[0]):
        dthdx[i, :, :], dthdy[i, :, :] = mpcalc.gradient(theta_w_smooth[i, :, :], axes=[-1, -2], deltas=(dx, dy))
    
    tfp, mag_dth = calculate_tfp(dthdx, dthdy, lons, lats)
    
    vf = calculate_vf(u, v, tfp, lons, lats)
       
    output_directory = Path(output_directory_fronts) / 'tfp_files'
    output_directory.mkdir(parents=True, exist_ok=True)
    output_filepath = output_directory / f'tfp_{model_name}.nc'
    
    if os.path.exists(output_filepath):
        os.remove(output_filepath)
    
    save_to_netcdf(output_filepath, lons, lats, ds.time, tfp, mag_dth, vf)