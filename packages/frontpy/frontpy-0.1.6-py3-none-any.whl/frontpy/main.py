from .download_data import download_gfs_data
from .calc_tfp import process_tfp
from .front_ident import front_identification, tfp_masks, open_tfp
from .plot_fronts import plot_fronts_satellite
from .make_gif import gif
from pathlib import Path

def validate_inputs(config):
    if not (config['lat_min'] < config['lat_max']):
        raise ValueError("lat_min must be less than lat_max")
    if not (config['lon_min'] < config['lon_max']):
        raise ValueError("lon_min must be less than lon_max")
    
def main(config):
    validate_inputs(config)
    if config['model_name'] == "GFS":
        ds = download_gfs_data(config['output_directory_fronts'],config['pressure'],config['lat_max'], config['lat_min'], config['lon_max'], config['lon_min'], config['start_date'], config['end_date'])

        process_tfp(ds, config['model_name'], config['output_directory_fronts'], config['pressure'], config['smooth_sigma'])
    
        tfp_filepath = Path(config['output_directory_fronts']) / f"tfp_files/tfp_{config['model_name']}.nc"
        tfp, mag_thetaw, vf = open_tfp(tfp_filepath)
        tfp_cold, tfp_warm = tfp_masks(tfp, mag_thetaw, vf, config['thetaw_thresh'], config['vf_thresh'])
        ff, fq = front_identification(tfp_cold, tfp_warm, config['line_or_area'], config['min_points'], config['min_length'], config['output_directory_fronts'])
    else:
        raise ValueError("Currently only GFS 0.25 Degree Global Forecast 0.25 data is supported.")
    
    return ff, fq

def plot_results(ff, fq, config):
    plot_fronts_satellite(ff, fq, config['line_or_area'], config['lat_max'], config['lat_min'], config['lon_max'], config['lon_min'], config['min_area'], config['output_directory_fronts'])
    gif(config['start_date'], config['end_date'], config['frame_rate'], config['line_or_area'], config['output_directory_fronts'])