import os
import numpy as np
from pathlib import Path
import colorsys
import boto3
from botocore import UNSIGNED
from botocore.config import Config
from datetime import datetime
from osgeo import osr
from osgeo import gdal

def get_CMI_GOES16(yyyymmddhhmn, band, output_dir):

    os.makedirs(output_dir, exist_ok=True)

    year = datetime.strptime(yyyymmddhhmn, '%Y%m%d%H%M').strftime('%Y')
    day = datetime.strptime(yyyymmddhhmn, '%Y%m%d%H%M').strftime('%j')
    hour = datetime.strptime(yyyymmddhhmn, '%Y%m%d%H%M').strftime('%H')
    min = datetime.strptime(yyyymmddhhmn, '%Y%m%d%H%M').strftime('%M')
    

    bucket = 'noaa-goes16'
    product = 'ABI-L2-CMIPF'

    s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    prefix = f'{product}/{year}/{day}/{hour}/OR_{product}-M6C{int(band):02.0f}_G16_s{year}{day}{hour}{min}'

    s3_list_objects = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter = "/")

    if 'Contents' not in s3_list_objects: 
        print(f'There are no files for the date: {yyyymmddhhmn}, Band-{band}.')
        return -1
    else:
        for obj in s3_list_objects['Contents']: 
            key = obj['Key']
            name = key.split('/')[-1].split('.')[0]

            file_path = Path(output_dir) / f'{name}.nc'

            if file_path.exists():
                print(f'File {file_path} already exists.')
            else:
                print(f'Downloading: {file_path}')
                s3_client.download_file(bucket, key, str(file_path))

    return f'{name}'

def reproject_img(output_file, nc_file, data_array, region_extent, no_data_value):

    src_proj = osr.SpatialReference()
    src_proj.ImportFromProj4(nc_file.GetProjectionRef())

    dst_proj = osr.SpatialReference()
    dst_proj.ImportFromProj4("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")
   
    geo_transform = nc_file.GetGeoTransform()
    mem_driver = gdal.GetDriverByName('MEM')
    temp_ds = mem_driver.Create('temp', data_array.shape[0], data_array.shape[1], 1, gdal.GDT_Float32)
    temp_ds.SetGeoTransform(geo_transform)
    temp_ds.GetRasterBand(1).WriteArray(data_array)

    warp_options = {'format': 'netCDF',
                    'srcSRS': src_proj,
                    'dstSRS': dst_proj,
                    'outputBounds': (region_extent[0], region_extent[3], region_extent[2], region_extent[1]),
                    'outputBoundsSRS': dst_proj,
                    'outputType': gdal.GDT_Float32,
                    'srcNodata': no_data_value,
                    'dstNodata': 'nan',
                    'resampleAlg': gdal.GRA_NearestNeighbour}

    gdal.Warp(output_file, temp_ds, **warp_options)

def read_color_palette(path):
    try:
        with open(path) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File {path} not found")
        return None

    x, r, g, b = [], [], [], []
    colorModel = 'RGB'

    for line in lines:
        if line.startswith('#'):
            if line.strip().endswith('HSV'):
                colorModel = 'HSV'
            continue
        
        parts = line.split()
        
        if parts[0] in ['B', 'F', 'N']:
            continue
        
        x.append(float(parts[0]))
        r.append(float(parts[1]))
        g.append(float(parts[2]))
        b.append(float(parts[3]))

        x.append(float(parts[4]))
        r.append(float(parts[5]))
        g.append(float(parts[6]))
        b.append(float(parts[7]))

    x = np.array(x)
    r = np.array(r)
    g = np.array(g)
    b = np.array(b)

    if colorModel == 'HSV':
        for i in range(r.shape[0]):
            rr, gg, bb = colorsys.hsv_to_rgb(r[i] / 360.0, g[i], b[i])
            r[i], g[i], b[i] = rr, gg, bb

    if colorModel == 'RGB':
        r, g, b = r / 255.0, g / 255.0, b / 255.0

    xNorm = (x - x[0]) / (x[-1] - x[0])

    colorDict = {
        'red':   [[xNorm[i], r[i], r[i]] for i in range(len(x))],
        'green': [[xNorm[i], g[i], g[i]] for i in range(len(x))],
        'blue':  [[xNorm[i], b[i], b[i]] for i in range(len(x))]
    }

    return colorDict

