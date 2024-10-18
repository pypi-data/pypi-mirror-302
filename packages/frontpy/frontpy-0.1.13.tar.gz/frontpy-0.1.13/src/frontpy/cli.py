import os
import typer
from enum import Enum
from datetime import datetime
from .main import main, plot_results

main_cli = typer.Typer()

class LineOrArea(str, Enum):
    line = "line"
    area = "area"

class Mode(str, Enum):
    identify = "identify"
    plot = "plot"
    both = "both"

def validate_date(date_str: str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d %H')
        return date_str
    except ValueError:
        raise typer.BadParameter("Date must be in the format YYYY-MM-DD HH")

#@main_cli.command()
@main_cli.command(
    context_settings={"ignore_unknown_options": True}
)
def run(
    start_date: str = typer.Argument(..., help="Start date and time for the analysis (format: YYYY-MM-DD HH)", callback=validate_date),
    end_date: str = typer.Argument(..., help="End date and time for the analysis (format: YYYY-MM-DD HH)", callback=validate_date),
    lat_max: str = typer.Argument(..., help="Maximum latitude for the analysis area (degrees, range: -90 to 90)"),
    lat_min: str = typer.Argument(..., help="Minimum latitude for the analysis area (degrees, range: -90 to 90)"),
    lon_max: str = typer.Argument(..., help="Maximum longitude for the analysis area (degrees, range: -180 to 180)"),
    lon_min: str = typer.Argument(..., help="Minimum longitude for the analysis area (degrees, range: -180 to 180)"),
    line_or_area: LineOrArea = typer.Argument(..., help="Type of representation for the fronts (line or area)"),
    output_directory_fronts: str = typer.Argument(..., help="Path to your output directory"),
    mode: Mode = typer.Argument(..., help="Choose which task to perform: 'identify', 'plot', or 'both'"),
    
    # Optional arguments
    model_name: str = typer.Option(None, help="Name of the dataset to be used. Options available: ERA5, GFS or None). Choose None or leave it blank if you want to use your own files"),
    filepath: str = typer.Option(None, help="Path to the local NetCDF file containing u, v, specific humidity and temperature (required if model_name is None)"),
    pressure: str = typer.Option(850, help="Atmospheric pressure level (hPa) at which front identification is performed"),
    thetaw_thresh: str = typer.Option(3.0, help="Threshold for the magnitude of the gradient of potential wet-bulb temperature (K/100km) for front identification"),
    vf_thresh: str = typer.Option(1.0, help="Threshold for wind velocity (m/s) for front classification as cold or warm front"),
    smooth_sigma: str = typer.Option(0.5, help="Smoothing parameter (sigma) for Gaussian filtering"),
    min_points: str = typer.Option(4, help="Minimum number of frontal points required for a valid frontal line"),
    min_length: str = typer.Option(500, help="Minimum length (km) for the frontal line to be considered"),
    min_area: str = typer.Option(5000, help="Minimum area (km²) that a frontal zone must occupy to be considered"),
    frame_rate: str = typer.Option(3, help="Frame rate (frames per second) for the animation; higher rates result in a faster animation"),


):
    """This is the CLI for the identification of atmospheric fronts from FrontPy package, allowing users to specify parameters for analysis and visualization directly from the command line."""

    if model_name is None and filepath is None:
        raise typer.BadParameter("If model_name is None, a filepath to the local NetCDF file containing u, v, specific humidity and temperature must be provided.")
    
    config = {
        "start_date": start_date,
        "end_date": end_date,
        "lat_max": float(lat_max),
        "lat_min": float(lat_min),
        "lon_max": float(lon_max),
        "lon_min": float(lon_min),
        "model_name": model_name,
        "filepath": filepath,
        "pressure": int(pressure),
        "thetaw_thresh": float(thetaw_thresh),
        "vf_thresh": float(vf_thresh),
        "smooth_sigma": float(smooth_sigma),
        "line_or_area": line_or_area,
        "min_points": int(min_points),
        "min_length": float(min_length),
        "min_area": float(min_area),
        "frame_rate": float(frame_rate),
        "output_directory_fronts": output_directory_fronts
    }

    if mode == Mode.identify or mode == Mode.both:
        ff, fq = main(config)
        if mode == Mode.both:
            plot_results(ff, fq, config)
    elif mode == Mode.plot:
        cold_fronts_path = os.path.join(config['output_directory_fronts'], "cold_fronts.csv")
        warm_fronts_path = os.path.join(config['output_directory_fronts'], "warm_fronts.csv")
        
        if not os.path.exists(cold_fronts_path) or not os.path.exists(warm_fronts_path):
            raise FileNotFoundError("The files containing the front dataframes (cold_fronts.csv and/or warm_fronts.csv) were not found in the specified directory. Please run the main function to generate both dataframes.")

        import pandas as pd
        ff = pd.read_csv(cold_fronts_path)
        fq = pd.read_csv(warm_fronts_path)

        plot_results(ff, fq, config)

if __name__ == "__main__":
    main_cli()