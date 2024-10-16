import io
import xarray as xr
from siphon.catalog import TDSCatalog
from datetime import datetime
from pathlib import Path

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

    lat_max += 5
    lat_min -= 5
    lon_max += 5
    lon_min -= 5

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

    output_filepath = output_directory / f"frontvars_{start_date_str}_{end_date_str}.nc"
    ds.to_netcdf(output_filepath) 

    print(f"Data saved in: {output_directory}")
    return ds