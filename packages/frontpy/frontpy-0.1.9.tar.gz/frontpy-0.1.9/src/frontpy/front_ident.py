import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.path import Path
from pathlib import Path as Path2
from osgeo import gdal

from cartopy.util import add_cyclic_point
from shapely.geometry import Polygon
import geopandas as gpd
import xarray as xr
import warnings
plt.switch_backend('agg')
warnings.filterwarnings("ignore", category=DeprecationWarning)
gdal.PushErrorHandler('CPLQuietErrorHandler')

def create_paths(f):
    paths_by_layer = []
    for i, joined_paths_in_layer in enumerate(f.get_paths()):
        separated_paths_in_layer = []
        path_vertices = []
        path_codes = []
        for verts, code in joined_paths_in_layer.iter_segments():
            if code == Path.MOVETO:
                if path_vertices:
                    separated_paths_in_layer.append(Path(np.array(path_vertices), np.array(path_codes)))
                path_vertices = [verts]
                path_codes = [code]
            elif code == Path.LINETO:
                path_vertices.append(verts)
                path_codes.append(code)
            elif code == Path.CLOSEPOLY:
                path_vertices.append(verts)
                path_codes.append(code)
        if path_vertices:
            separated_paths_in_layer.append(Path(np.array(path_vertices), np.array(path_codes)))

        paths_by_layer.append(separated_paths_in_layer)

    return paths_by_layer

def create_paths_dataframe(paths_by_layer, data, tipo):
    all_paths_data = []
    path_id = 1

    for layer_paths in paths_by_layer:
        for individual_path in layer_paths:
            vertices = individual_path.vertices
            lons = vertices[:, 0]
            lats = vertices[:, 1]

            data_values = data.values if hasattr(data, 'values') else data

            temp_df = pd.DataFrame({
                "id": path_id,
                "lat": lats,
                "lon": lons,
                "data": data_values,
                "tipo": tipo
            })
            all_paths_data.append(temp_df)
            path_id += 1

    if all_paths_data:
        df_paths = pd.concat(all_paths_data, ignore_index=True)
        df_paths['data'] = pd.to_datetime(df_paths['data'], format='%Y-%m-%d %H:%M:%S')
    else:
        df_paths = pd.DataFrame()

    return df_paths

def generate_unique_ids(df):
    df.loc[:, 'id'] = df.groupby(['data', 'id']).ngroup() + 1
    return df

def calcular_area(df):
    polygons = []
    for id, group in df.groupby('id'):
        polygon = Polygon(zip(group['lon'], group['lat']))
        polygons.append({'id': id, 'geometry': polygon})

    gdf = gpd.GeoDataFrame(polygons, crs="EPSG:4326") 
    gdf = gdf.to_crs(epsg=3395)

    gdf['area_km2'] = gdf['geometry'].area / 1e6

    area_dict = gdf[['id', 'area_km2']].drop_duplicates().set_index('id').to_dict()['area_km2']
    
    df_copy = df.copy()
    df_copy['area_km2'] = df_copy['id'].map(area_dict)
    
    return df_copy

def haversine(lon1, lat1, lon2, lat2): 
    lon1 = np.deg2rad(lon1)
    lon2 = np.deg2rad(lon2)
    lat1 = np.deg2rad(lat1)
    lat2 = np.deg2rad(lat2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371.0
    return (c * r)

def calculate_length(group):
    group = group.reset_index(drop=True)

    if len(group) > 1:
        length = haversine(group['lon'].values[:-1], group['lat'].values[:-1],
                           group['lon'].values[1:], group['lat'].values[1:]).sum()
        return length
    return 0

def filter_by_length(df, min_length):
    lengths = df.groupby(['data', 'id']).apply(calculate_length).reset_index()
    lengths.columns = ['data', 'id', 'length']

    filtered_lengths = lengths[lengths['length'] >= min_length]

    filtered_df = df[df['id'].isin(filtered_lengths['id']) & df['data'].isin(filtered_lengths['data'])].reset_index(drop=True)
    
    return filtered_df

def open_tfp(tfp_file):
    tfp_vars = xr.open_dataset(tfp_file)
    tfp = tfp_vars.tfp
    mag_thetaw = tfp_vars.mag_thetaw
    vf = tfp_vars.vf
    return tfp, mag_thetaw, vf

def tfp_masks(tfp,mag_thetaw,vf,thetaw_thresh,vf_thresh):
    fcold = tfp.where((mag_thetaw>=thetaw_thresh)&(vf>=vf_thresh))
    fwarm = tfp.where((mag_thetaw>=thetaw_thresh)&(vf<=-vf_thresh))
    return fcold, fwarm

def front_identification(tfp_cold, tfp_warm, line_or_area, min_points, min_length, output_directory_fronts):
    all_dfs_contour = []
    all_dfs_contourf = []

    for t in tfp_cold.time:
        tfp_cold_2 = tfp_cold.sel(time=t)
        tfp_warm_2 = tfp_warm.sel(time=t)

        lon2 = tfp_cold_2.lon
        lat2 = tfp_cold_2.lat
        tfp_cold_3, lon3 = add_cyclic_point(tfp_cold_2, coord=lon2)

        f_contour = plt.contour(lon3, lat2, tfp_cold_3, levels=1, colors="blue")
        f_contourf = plt.contourf(lon3, lat2, tfp_cold_3, levels=1, colors="blue", alpha=0.5)

        lon4 = tfp_warm_2.lon
        lat4 = tfp_warm_2.lat
        tfp_warm_3, lon5 = add_cyclic_point(tfp_warm_2, coord=lon4)

        f2_contour = plt.contour(lon5, lat4, tfp_warm_3, levels=1, colors="red")
        f2_contourf = plt.contourf(lon5, lat4, tfp_warm_3, levels=1, colors="red", alpha=0.5)

        fcolds_paths_contour = create_paths(f_contour)
        fcolds_paths_contourf = create_paths(f_contourf)

        fwarms_paths_contour = create_paths(f2_contour)
        fwarms_paths_contourf = create_paths(f2_contourf)

        df_paths_fcolds_contour = create_paths_dataframe(fcolds_paths_contour, t, "cold")
        df_paths_fcolds_contourf = create_paths_dataframe(fcolds_paths_contourf, t, "cold")

        df_paths_fwarms_contour = create_paths_dataframe(fwarms_paths_contour, t, "warm")
        df_paths_fwarms_contourf = create_paths_dataframe(fwarms_paths_contourf, t, "warm")

        all_dfs_contour.append(pd.concat([df_paths_fcolds_contour, df_paths_fwarms_contour], axis=0).reset_index(drop=True))
        all_dfs_contourf.append(pd.concat([df_paths_fcolds_contourf, df_paths_fwarms_contourf], axis=0).reset_index(drop=True))

        plt.close()

    df_contour = pd.concat(all_dfs_contour, ignore_index=True)
    df_contourf = pd.concat(all_dfs_contourf, ignore_index=True)

    df_contour = generate_unique_ids(df_contour)
    df_contourf = generate_unique_ids(df_contourf)

    output_directory_fronts = Path2(output_directory_fronts)

    output_filepath1 = output_directory_fronts / "frontal_lines.csv"
    output_filepath2 = output_directory_fronts / "frontal_areas.csv"
    
    df_contour.to_csv(output_filepath1,index=False)
    df_contourf.to_csv(output_filepath2,index=False)

    ffs = []
    fqs = []
    
    for t in df_contour.data.unique():
        fronts = df_contour[df_contour.data==t]
        if line_or_area == "line":
            
            ff = fronts[fronts.tipo=="cold"]
            ff = ff.groupby('id').filter(lambda x: len(x) >= min_points)
            ff = filter_by_length(ff, min_length)
            ffs.append(ff)
            
            fq = fronts[fronts.tipo=="warm"]
            fq = fq.groupby('id').filter(lambda x: len(x) >= min_points)            
            fq = filter_by_length(fq, min_length)
            fqs.append(fq)

        elif line_or_area == "area":
            fronts = df_contourf[df_contourf.data==t]
            ff = fronts[fronts.tipo=="cold"]
            ff = ff.groupby('id').filter(lambda x: len(x) >= min_points)
            ffs.append(ff)

            fq = fronts[fronts.tipo=="warm"]
            fq = fq.groupby('id').filter(lambda x: len(x) >= min_points)
            fqs.append(fq)

        else:
            print("Erro: area_or_line só aceita 'area' ou 'line'.")

    combined_ff = pd.concat(ffs, ignore_index=True)
    combined_fq = pd.concat(fqs, ignore_index=True)
        
    return combined_ff, combined_fq