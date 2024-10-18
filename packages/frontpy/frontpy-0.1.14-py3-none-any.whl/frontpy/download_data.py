import io
import os
import xarray as xr
from siphon.catalog import TDSCatalog
from datetime import datetime
from pathlib import Path
import cdsapi
import pandas as pd

def download_gfs_data(output_directory_fronts,pressure,lat_max,lat_min,lon_max,lon_min,start_date=None,end_date=None):
    url = ('http://thredds.ucar.edu/thredds/catalog/grib/NCEP/GFS/'
           'Global_0p25deg/catalog.xml?dataset=grib/NCEP/GFS/Global_0p25deg/Best')

    best_gfs = TDSCatalog(url)
    best_ds = best_gfs.datasets[0]
    ncss = best_ds.subset()

    if start_date is None:
        raise ValueError("The start date must be provided in the format 'YYYY-MM-DD HH'.")
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d %H") 

    start_date = datetime.strptime(start_date, "%Y-%m-%d %H")
    end_date = datetime.strptime(end_date, "%Y-%m-%d %H")

    if start_date > end_date:
        raise ValueError("The start date cannot be later than the end date.")
    if end_date > datetime.now():
        raise ValueError("The end date cannot be in the future.")

    lat_max += 0
    lat_min -= 0
    lon_max += 0
    lon_min -= 0

    query = ncss.query()
    query.lonlat_box(north=lat_max, south=lat_min, east=lon_max, west=lon_min)
    query.time_range(start_date, end_date)
    query.variables('u-component_of_wind_isobaric',
                    'v-component_of_wind_isobaric',
                    'Temperature_isobaric',
                    'Specific_humidity_isobaric')
    query.vertical_level(pressure*100) 
    query.accept('netcdf4')

    data = ncss.get_data_raw(query)
    ds = xr.open_dataset(io.BytesIO(data)).metpy.parse_cf()

    vars_to_drop = [var for var in ds.data_vars if ds[var].dtype == 'int32']
    ds = ds.drop_vars(vars_to_drop)
    ds = ds.drop_vars('metpy_crs', errors='ignore')

    for coord in ds.coords:
        if ds[coord].attrs.get('standard_name') == 'time':
            ds = ds.rename({coord: 'time'})
            break

    ds = ds.rename({
        "Specific_humidity_isobaric": "hus",
        "Temperature_isobaric": "ta",
        "u-component_of_wind_isobaric": "ua",
        "v-component_of_wind_isobaric": "va",
        "latitude": "lat",
        "longitude": "lon"
    })

    ds = ds.sel(isobaric=pressure*100)

    start_date_str = start_date.strftime("%Y-%m-%d_%H")
    end_date_str = end_date.strftime("%Y-%m-%d_%H")

    output_directory = Path(output_directory_fronts) / 'tfp_files'
    output_directory.mkdir(parents=True, exist_ok=True)

    output_filepath = output_directory / f"GFS_frontvars_{start_date_str}_{end_date_str}.nc"

    if os.path.exists(output_filepath):
        os.remove(output_filepath)
    ds.to_netcdf(output_filepath) 

    print(f"Data saved in: {output_directory}")
    return ds

def download_era5_data(output_directory_fronts,pressure,lat_max,lat_min,lon_max,lon_min,start_date=None,end_date=None):
    if start_date is None:
        raise ValueError("The start date must be provided in the format 'YYYY-MM-DD HH'.")
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d %H") 

    start_date = datetime.strptime(start_date, "%Y-%m-%d %H")
    end_date = datetime.strptime(end_date, "%Y-%m-%d %H")

    if start_date > end_date:
        raise ValueError("The start date cannot be later than the end date.")
    if end_date > datetime.now():
        raise ValueError("The end date cannot be in the future.")

    lat_max += 0
    lat_min -= 0
    lon_max += 0
    lon_min -= 0

    time_range = pd.date_range(start=start_date, end=end_date, freq="3h")

    years = sorted(time_range.year.unique())
    months = sorted(time_range.month.unique())
    days = sorted(time_range.day.unique())
    hours = sorted(time_range.hour.unique())
    pressures = [str(pressure)]

    years = [str(year) for year in years]
    months = [str(month) for month in months]
    days = [str(day) for day in days]
    hours = [str(hour) + ":00" for hour in hours]

    dataset = "reanalysis-era5-pressure-levels"
    request = {
        "product_type": ["reanalysis"],
        "variable": [
            "specific_humidity",
            "temperature",
            "u_component_of_wind",
            "v_component_of_wind"
        ],
        "year": years,
        "month": months,
        "day": days,
        "time": hours, 
        "pressure_level": pressures,
        "data_format": "netcdf",
        "download_format": "unarchived",
        "area": [lat_max, lon_min, lat_min, lon_max]
    }

    start_date_str = start_date.strftime("%Y-%m-%d_%H")
    end_date_str = end_date.strftime("%Y-%m-%d_%H")

    output_directory = Path(output_directory_fronts) / 'tfp_files'
    output_directory.mkdir(parents=True, exist_ok=True)
    output_filepath_temp = output_directory / f"ERA5_temp_frontvars_{start_date_str}_{end_date_str}.nc"

    if os.path.exists(output_filepath_temp):
        os.remove(output_filepath_temp)

    client = cdsapi.Client()
    client.retrieve(dataset, request).download(output_filepath_temp)

    try:
        client.retrieve(dataset, request).download(output_filepath_temp)
    except Exception as e:
        print("Failed to retrieve data from CDS API, go to: https://cds.climate.copernicus.eu/how-to-api")
        raise RuntimeError(f'Error details: {e}')

    ds = xr.open_dataset(output_filepath_temp)

    for coord in ds.coords:
        if ds[coord].attrs.get('standard_name') == 'time':
            ds = ds.rename({coord: 'time'})
            break

    ds = ds.rename({
        "q": "hus",
        "t": "ta",
        "u": "ua",
        "v": "va",
        "latitude": "lat",
        "longitude": "lon"
    })

    ds = ds.sel(pressure_level=pressure)

    output_filepath = output_directory / f"ERA5_frontvars_{start_date_str}_{end_date_str}.nc"
    if os.path.exists(output_filepath):
        os.remove(output_filepath)
    ds.to_netcdf(output_filepath)

    os.remove(output_filepath_temp)

    print(f"Data saved in: {output_directory}")
    return ds