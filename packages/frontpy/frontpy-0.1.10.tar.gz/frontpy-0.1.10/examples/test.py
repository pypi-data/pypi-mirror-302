from frontpy import main, plot_results

config = {
    "start_date": "2024-10-12 00",
    "end_date": "2024-10-13 00",
    "lat_max": 20,
    "lat_min": -60,
    "lon_max": -20,
    "lon_min": -90,
    "model_name": "GFS",
    "thetaw_thresh": 3.0,
    "vf_thresh": 1.0,
    "line_or_area": "area",
    "min_points": 4,
    "min_length": 500,
    "pressure": 850,
    "smooth_sigma": 0.5,
    "min_area": 5000,
    "frame_rate": 2,
    "output_directory_fronts": "your_output_directory"
    }
    
ff, fq = main(config)

plot_results(ff,fq,config)
