# FrontPy

FrontPy is a Python package designed for the detection and analysis of atmospheric fronts. It uses the Thermal Front Parameter (TFP) method to identify cold and warm fronts. The package also includes visualization capabilities, allowing users to plot the identified fronts over GOES-16 satellite imagery.

Currently, only analysis and forecast data from the GFS 0.25 Degree Global Forecast model are supported.

## Installation of FrontPy

### Step 1: Create a new Conda environment

First, you should create a new environment with the specific version of Python and some necessary dependencies. Run the following command in your terminal or command prompt:

```bash
conda create -n your_environment_name python=3.9.15 gdal=3.3.3 poppler=21.09 -c conda-forge
```

Replace *your_environment_name* with your desired name for the environment. The conda will create an isolated environment with Python 3.9.15 and the gdal and poppler libraries, which are necessary for the functionality of FrontPy. This will ensure that FrontPy will run smoothly.

### Step 2: Activate your new Conda environment

Once the environment is created, activate it with the following command:

```bash
conda activate your_environment_name
```

### Step 3: Install FrontPy using pip

Now that you are in an isolated environment, install FrontPy using pip:

```bash
pip install frontpy
```

## Usage

To use FrontPy for detecting and analyzing atmospheric fronts, follow these steps:

**Step 1: Import the main and plot_results functions from the package**:

```python
from frontpy import main, plot_results
```

**Step 2: Set up the parameters required for downloading the data, calculating the Thermal Front Parameter (TFP), detecting cold and warm fronts, and final visualization**. 

The parameters must be provided in a dictionary, like the following:

```python
config = {
    "start_date": "2024-10-11 12",  # Start date and time for the analysis (format: YYYY-MM-DD HH) - string
    "end_date": "2024-10-12 12",    # End date and time for the analysis (format: YYYY-MM-DD HH) - string
    "lat_max": 20,                  # Maximum latitude for the analysis area (degrees, range: -90 to 90) - float
    "lat_min": -60,                 # Minimum latitude for the analysis area (degrees, range: -90 to 90) - float
    "lon_max": -20,                 # Maximum longitude for the analysis area (degrees, range: -180 to 180) - float
    "lon_min": -90,                 # Minimum longitude for the analysis area (degrees, range: -180 to 180) - float
    "model_name": "GFS",            # Name of the model to be used (currently only GFS 0.25 Degree Global Forecast 0.25 data is supported) - string
    "pressure": 850,                # [Default: 850] Atmospheric pressure level (hPa) at which front identification is performed - int
    "thetaw_thresh": 3.0,           # [Default: 3.0] Threshold for wet-bulb temperature (Celsius) for front identification -  float
    "vf_thresh": 1.0,               # [Default: 1.0] Threshold for wind velocity (m/s) for front classification as cold or warm front - float
    "smooth_sigma": 0.5,            # [Default: 0.5] Smoothing parameter (sigma) for Gaussian filtering - float
    "line_or_area": "area",         # Type of representation for the fronts (line or area) - string
    "min_points": 4,                # [Default: 4] Minimum number of frontal points required for a valid frontal line - int
    "min_length": 500.0,            # [Default: 500.0] Minimum length (km) for the frontal line to be considered - float
    "min_area": 5000.0,             # [Default: 5000.0] Minimum area (km²) for the frontal line to be considered - float
    "frame_rate": 3.0,              # [Default: 3.0] Frame rate (frames per second) for the generated animation; higher rates result in a faster animation - float
    "output_directory_fronts": "path_to_your_chosen_output_directory"   # Path to your output directory
}
```

Currently, the default values have only been tested for the Southern Hemisphere.

**Note:** Be carefull with the amount of smoothing applied to the data. It is recommended to use the default value (0.5).


**Step 3: Call the main function**:

The *main* function will return two Pandas dataframes: one for cold fronts and one for warm fronts.

So, you can call the main function like this:

```python
cold_fronts, warm_fronts = main(config)
```

**Step 4: Plot the images and generate an animation**:

Lastly, you can plot the results and generate an animation using the *plot_results* function. The images and animation will be saved in your output directory.

```    
plot_results(cold_fronts, warm_fronts, config)
```

### Command Line Interface (CLI)

FrontPy also supports command-line execution through the *cli.py* file. This allows users to specify parameters for analysis and visualization directly from the command line.

To run FrontPy using the CLI, execute the following command in your terminal (without the <>):

```bash
fronts <start_date> <end_date> <lat_max> <lat_min> <lon_max> <lon_min> <line_or_area> <output_directory_fronts>
```

The above arguments are mandatory and must be provided in string format and in the specified order. Optional arguments can also be included using the following prefixes before the values of your choice:

- `--model-name`
- `--pressure`
- `--thetaw-thresh`
- `--vf-thresh`
- `--smooth-sigma`
- `--min-points`
- `--min-length`
- `--min-area`
- `--frame-rate`

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for more details.
