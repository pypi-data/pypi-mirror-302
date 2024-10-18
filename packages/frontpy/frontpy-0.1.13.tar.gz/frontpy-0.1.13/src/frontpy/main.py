from .download_data import download_gfs_data, download_era5_data
from .calc_tfp import process_tfp
from .front_ident import front_identification, tfp_masks, open_tfp
from .plot_fronts import plot_fronts_satellite
from .make_gif import gif
from pathlib import Path
import xarray as xr

def validate_inputs(config):
    """Valida entradas principais."""
    if config['lat_min'] >= config['lat_max']:
        raise ValueError("lat_min must be less than lat_max")
    if config['lon_min'] >= config['lon_max']:
        raise ValueError("lon_min must be less than lon_max")
    if config['model_name'] is None and 'filepath' not in config:
        raise ValueError("If model_name is None, a filepath must be provided.")
        
def adjust_lat_lon(ds, config):
    """Ajusta latitudes e longitudes para os formatos esperados."""
    if 'longitude' in ds.coords:
        ds = ds.rename({"longitude": "lon"})
    if 'latitude' in ds.coords:
        ds = ds.rename({"latitude": "lat"})

    if (ds.coords['lon'] >= 0).all() and (ds.coords['lon'] <= 360).all():
        ds.coords['lon'] = (ds.coords['lon'] + 180) % 360 - 180
        ds = ds.sortby(ds.lon)
    else:
        ds = ds.sortby(ds.lon)

    ds = ds.sortby('lat',ascending=False)

    ds = ds.sel(lat=slice(config['lat_max'], config['lat_min']),
                lon=slice(config['lon_min'], config['lon_max']))
    return ds

def expand_bounds(config, margin=5):
    """Expande os limites de latitude e longitude por uma margem fixa."""
    config['lat_max'] += margin
    config['lat_min'] -= margin
    config['lon_max'] += margin
    config['lon_min'] -= margin

def load_data(config):
    """Carrega os dados dependendo do modelo ou caminho do arquivo."""
    if config['model_name'] == "GFS":
        return download_gfs_data(config['output_directory_fronts'], config['pressure'],
                                 config['lat_max'], config['lat_min'],
                                 config['lon_max'], config['lon_min'],
                                 config['start_date'], config['end_date'])
    elif config['model_name'] == "ERA5":
        return download_era5_data(config['output_directory_fronts'], config['pressure'],
                                  config['lat_max'], config['lat_min'],
                                  config['lon_max'], config['lon_min'],
                                  config['start_date'], config['end_date'])
    elif config['model_name'] is None:
        ds = xr.open_dataset(config['filepath'])
        ds = adjust_lat_lon(ds, config)
        return ds
    else:
        raise ValueError("Invalid model_name or no data found.")

def process_fronts(ds, config):
    """Processa os dados do TFP e identifica as frentes."""
    process_tfp(ds, config['start_date'], config['end_date'], config['model_name'],
                config['output_directory_fronts'], config['pressure'], config['smooth_sigma'])
    
    if config['model_name'] is None:
        modelname = "MyData"
        tfp_filepath = Path(config['output_directory_fronts']) / f"tfp_files/tfp_{modelname}.nc"
    else:
        tfp_filepath = Path(config['output_directory_fronts']) / f"tfp_files/tfp_{config['model_name']}.nc"
    tfp, mag_thetaw, vf = open_tfp(tfp_filepath)
    
    tfp_cold, tfp_warm = tfp_masks(tfp, mag_thetaw, vf, config['thetaw_thresh'], config['vf_thresh'])
    
    ff, fq = front_identification(tfp_cold, tfp_warm, config['line_or_area'],
                                  config['min_points'], config['min_length'],
                                  config['output_directory_fronts'])
    return ff, fq

def plot_results(ff, fq, config):
    """Plota e gera GIF das frentes identificadas."""
    plot_fronts_satellite(config['model_name'], ff, fq, config['line_or_area'],
                          config['lat_max'], config['lat_min'],
                          config['lon_max'], config['lon_min'], config['min_area'],
                          config['output_directory_fronts'])
    
    gif(config['model_name'], config['start_date'], config['end_date'], config['frame_rate'],
        config['line_or_area'], config['output_directory_fronts'])

def main(config):
    """Função principal que executa todo o pipeline de processamento."""
    validate_inputs(config)
    #expand_bounds(config) 
    ds = load_data(config)
    ff, fq = process_fronts(ds, config)
    return ff, fq
