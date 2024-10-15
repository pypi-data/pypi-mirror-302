from metpy.units import units
import xarray as xr
import metpy.calc as mpcalc
import numpy as np
import os
from scipy.ndimage import gaussian_filter
from pathlib import Path


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
    mag_dth = np.sqrt(dthdx**2 + dthdy**2)
    dthdx2 = dthdx / mag_dth
    dthdy2 = dthdy / mag_dth
    
    dthdx_mag, dthdy_mag = mpcalc.gradient(mag_dth, axes=[-1,-2],coordinates=[lons,lats])
    
    tfp = -1 * (dthdx_mag * dthdx2 + dthdy_mag * dthdy2)
    return tfp, mag_dth

def calculate_vf(u, v, tfp, lons, lats):
    dtfpdx, dtfpdy = mpcalc.gradient(tfp, axes=[-1,-2],coordinates=[lons,lats])
    mag_dtfp = np.sqrt(dtfpdx**2 + dtfpdy**2)
    
    vf = (u * dtfpdx / mag_dtfp) + (v * (dtfpdy / mag_dtfp))

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

def process_tfp(ds, model_name, output_directory_fronts, pressure=850, smooth_sigma=0.5):    
    if 'longitude' in ds.coords:
        ds = ds.rename({"longitude": "lon"})
    if 'latitude' in ds.coords:
        ds = ds.rename({"latitude": "lat"})

    ta = ds.ta
    hus = ds.hus
    u = ds.ua
    v = ds.va
    
    lons = ds.lon
    lats = ds.lat
    
    theta_w = calculate_theta_w(ta, hus, pressure)
    theta_w_smooth = gaussian_smoothing(theta_w, sigma=smooth_sigma)
    
    dthdx, dthdy = mpcalc.gradient(theta_w_smooth, axes=[-1, -2], coordinates=[lons, lats])
    
    tfp, mag_dth = calculate_tfp(dthdx, dthdy, lons, lats)
    
    vf = calculate_vf(u, v, tfp, lons, lats)
       
    output_directory = Path(output_directory_fronts) / 'tfp_files'
    output_directory.mkdir(parents=True, exist_ok=True)
    output_filepath = output_directory / f'tfp_{model_name}.nc'
    
    if os.path.exists(output_filepath):
        os.remove(output_filepath)
    
    save_to_netcdf(output_filepath, lons, lats, ds.time, tfp, mag_dth, vf)