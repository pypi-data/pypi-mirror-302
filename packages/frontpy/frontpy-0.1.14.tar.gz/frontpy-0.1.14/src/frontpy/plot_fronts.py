import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
from matplotlib import rcParams
from osgeo import gdal
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from netCDF4 import Dataset
from scipy.interpolate import UnivariateSpline

from .utils import get_CMI_GOES16, reproject_img, read_color_palette
from .front_ident import calc_area

plt.switch_backend('agg')
rcParams['font.family'] = 'serif'
rcParams['font.sans-serif'] = ['DejaVu Sans']

warnings.filterwarnings("ignore", category=DeprecationWarning)
gdal.PushErrorHandler('CPLQuietErrorHandler')


root = Path(__file__).resolve().parents[0]  
data_folder = root / 'resources'
palette_path = data_folder / 'IR_colormap.cpt'
palette = read_color_palette(palette_path)

cmap = cm.colors.LinearSegmentedColormap('cpt', palette)
colors_list_hex = [cm.colors.rgb2hex(cmap(i / 255)) for i in range(256)]
new_colors = colors_list_hex[19:]
cmap = ListedColormap(new_colors)


def plot_fronts_satellite(model_name, ff, fq, line_or_area, lat_max, lat_min, lon_max, lon_min, min_area, output_directory_fronts):
    if model_name is None:
        model_name = "MyData"
    inputdata = Path(output_directory_fronts) / 'originals'
    outputdata = Path(output_directory_fronts) / 'finals'
    input_directory = Path(output_directory_fronts) / 'figures'

    inputdata.mkdir(parents=True, exist_ok=True)
    outputdata.mkdir(parents=True, exist_ok=True)
    input_directory.mkdir(parents=True, exist_ok=True) 


    times_fronts = np.unique(ff.data.values)
    times_images = pd.to_datetime(ff.data).dt.strftime('%Y%m%d%H').unique()

    extent = [lon_min, lat_min, lon_max, lat_max]
    img_extent = [extent[0], extent[2], extent[1], extent[3]]

    k = 0
    for i,j in zip(times_images,times_fronts):
        time_img = i + '00'
        file_CMI = get_CMI_GOES16(time_img, 13, inputdata)
        var = 'CMI'
        img = gdal.Open(f'NETCDF:{inputdata}/{file_CMI}.nc:' + var)

        metadata = img.GetMetadata()
        scale = float(metadata.get(var + '#scale_factor'))
        offset = float(metadata.get(var + '#add_offset'))
        undef = float(metadata.get(var + '#_FillValue'))

        ds_cmi = img.ReadAsArray(0, 0, img.RasterXSize, img.RasterYSize).astype(float)
        ds_cmi = (ds_cmi * scale + offset) - 273.15

        filename_IR = f'{outputdata}/IR_{time_img}.nc'
        reproject_img(filename_IR, img, ds_cmi, extent, undef)

        ds = Dataset(filename_IR)
        ds2 = ds.variables['Band1'][:]

        #############################################################################################

        plt.figure(figsize=(12,16))

        ax = plt.axes(projection=ccrs.PlateCarree())

        ax.set_extent(img_extent, ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidths=1.2)
        ax.add_feature(cfeature.BORDERS.with_scale('50m'), linewidths=1.2)
        ax.add_feature(cfeature.STATES.with_scale('50m'), linewidths=0.5)
        img_plot = ax.imshow(ds2, origin='upper', vmin=-90, vmax=90, extent=img_extent, cmap=cmap, alpha=1.0)

        ff2 = ff[ff.data==j]
        fq2 = fq[fq.data==j]

        if line_or_area == "line":
            for id, track in ff2.groupby('id'):
                lat_cold = track['lat'].values
                lon_cold = track['lon'].values

                if len(lat_cold) < 4 or len(lon_cold) < 4:
                    print(f"Aviso: Não há pontos suficientes para interpolação para a frente cold id {id}.")
                    ax.plot(lon_cold, lat_cold, color='blue', linewidth=3, transform=ccrs.Geodetic(), zorder=99)
                    continue

                spline_lat = UnivariateSpline(np.arange(len(lat_cold)), lat_cold, s=1, k=2)
                spline_lon = UnivariateSpline(np.arange(len(lon_cold)), lon_cold, s=1, k=2)

                new_indices = np.linspace(0, len(lat_cold) - 1, num=100)
                lat_cold_smooth = spline_lat(new_indices)
                lon_cold_smooth = spline_lon(new_indices)

                ax.plot(lon_cold_smooth, lat_cold_smooth, color='blue', linewidth=3, transform=ccrs.Geodetic(), zorder=99)

            for id, track in fq2.groupby('id'):
                lat_warm = track['lat'].values
                lon_warm = track['lon'].values

                if len(lat_warm) < 4 or len(lon_warm) < 4:
                    print(f"Aviso: Não há pontos suficientes para interpolação para a frente warm id {id}.")
                    ax.plot(lon_warm, lat_warm, color='red', linewidth=3, transform=ccrs.Geodetic(), zorder=99)
                    continue

                spline_lat = UnivariateSpline(np.arange(len(lat_warm)), lat_warm, s=1, k=2)
                spline_lon = UnivariateSpline(np.arange(len(lon_warm)), lon_warm, s=1, k=2)

                new_indices = np.linspace(0, len(lat_warm) - 1, num=100)
                lat_warm_smooth = spline_lat(new_indices)
                lon_warm_smooth = spline_lon(new_indices)

                ax.plot(lon_warm_smooth, lat_warm_smooth, color='red', linewidth=3, transform=ccrs.Geodetic(), zorder=99)

        elif line_or_area == "area":
            ff2_area = calc_area(ff2)
            fq2_area = calc_area(fq2)

            ff2_filtered = ff2_area[ff2_area.area_km2>=min_area]
            fq2_filtered = fq2_area[fq2_area.area_km2>=min_area]

            for id, track in ff2_filtered.groupby('id'):
                lat_cold = track['lat'].values
                lon_cold = track['lon'].values

                ax.fill(lon_cold, lat_cold, 'blue', alpha=1, transform=ccrs.PlateCarree(), zorder=99)

            for id, track in fq2_filtered.groupby('id'):
                lat_warm = track['lat'].values
                lon_warm = track['lon'].values

                ax.fill(lon_warm, lat_warm, 'red', alpha=1, transform=ccrs.PlateCarree(), zorder=99)

        else:
            print("Error: area_or_line only accepts 'area' or 'line'.")

        gl = ax.gridlines(crs=ccrs.PlateCarree(), color='white', alpha=1.0, linestyle='--',
                          linewidth=0.25, xlocs=np.arange(-180, 180, 10),
                          ylocs=np.arange(-90, 90, 10), draw_labels=True)
        gl.top_labels = False
        gl.right_labels = False
        cb = plt.colorbar(img_plot, extend='both', orientation='vertical',
                     pad=0.02, shrink=0.5)
        
        ticks = np.linspace(-90, 90, 10)
        cb.set_ticks(ticks)
        cb.set_ticklabels(ticks)
        cb.set_label("Brightness Temperature (°C)", fontsize=12)
        ax.set_title('GOES-16 Infrared | Band 13',
                    fontsize=14, loc='left',fontweight='bold')

        formatted_date = pd.to_datetime(j).strftime("%d %B %Y - %HZ")

        ax.set_title(formatted_date, loc='right', color='k', fontsize=12)

        plt.savefig(f'{input_directory}/{model_name}_fronts_satellite_{line_or_area}_{i}.png', bbox_inches='tight',facecolor='white', dpi=200)
        print(f"**** Figure #{i} saved in: {input_directory} ****")
        plt.close()
        k += 1