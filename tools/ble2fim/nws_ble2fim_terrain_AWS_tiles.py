#!/usr/bin/env python
# coding: utf-8
#
# Purpose:
# From a user supplied area shapefile (multiple polygons),
# get the terrain data from the AWS registry of Open Data
# https://registry.opendata.aws/terrain-tiles/
#
# Output generated:
# DEM of the for each polygon.  Will return in the polygon's
# cooredinate reference system
#
# Created by: Andy Carter, PE
# Last revised - 2021.06.07

import geopandas as gpd
import requests
import json
import time

import rasterio
from rasterio.merge import merge

import rioxarray as rxr
import math
import os

# path to input shapefile
STR_LOAD_PATH = r'E:\X-NWS-Bathy\HUC_0504_Terrain\\'
STR_SHP_FILENAME = 'AOI_lidar_AR.shp'

# set to True to convert vertical data from meters to feet
B_CONVERT_TO_VERT_FT = True

STR_OUTPUT_DIR = r'C:\Test_Terrain\AWS_Scrape\\'
STR_SAVE_DEM_NAME = 'created_terrain'

str_boundary = STR_LOAD_PATH + STR_SHP_FILENAME

wgs = "epsg:4326"
int_zoom = 14 #the most detailed AWS Terrain level available

# load the subject request shapefile
gdf_boundary_prj = gpd.read_file(str_boundary)
str_crs_boundary = str(gdf_boundary_prj.crs) # projection of input area shapefile

gdf_boundary_wgs = gdf_boundary_prj.to_crs(wgs)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
def fn_deg2num(lat_deg, lon_deg, zoom):
    
    """Return the tile number (x,y) given the Lat/Long and zoom level

    Args:
        lat_deg: Point latitude in decimal degrees
        lon_deg: Point longitude in decimal degrees
        zoom: Tile pyramid zoom-in level 

    Returns:
        Integers of the x/y of the tile
    """
    
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def fn_get_features(gdf,int_poly_index):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    return [json.loads(gdf.to_json())['features'][int_poly_index]['geometry']]
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

for index, row in gdf_boundary_prj.iterrows():
    int_gdf_item = index
    
    # get the bounding box for each polygon in geodataframe
    flt_min_long, flt_min_lat, flt_max_long, flt_maxLat =  gdf_boundary_wgs['geometry'][int_gdf_item].bounds
    
    #indecies of tiles from within the bounding box
    int_x_min_tile = fn_deg2num(flt_min_lat,flt_min_long,int_zoom)[0]
    int_x_max_tile = fn_deg2num(flt_maxLat,flt_max_long,int_zoom)[0]

    int_y_min_tile = fn_deg2num(flt_min_lat,flt_min_long,int_zoom)[1]
    int_y_max_tile = fn_deg2num(flt_maxLat,flt_max_long,int_zoom)[1]
    
    #Create URL list of all the needed tiles
    list_terrain_paths = []
    for x in range(int_x_min_tile, int_x_max_tile + 1):
        for y in range (int_y_max_tile, int_y_min_tile + 1):

            str_url = r'https://s3.amazonaws.com/elevation-tiles-prod/geotiff/'
            str_url += str(int_zoom) + "/"
            str_url += str(x) + "/"
            str_url += str(y) + ".tif"
            list_terrain_paths.append(str_url)
    
    list_filenames_to_merge = []

    int_count = 1
    for i in list_terrain_paths:

        str_file_name = "AWS_" + str(int_gdf_item) + '_TileImage_' + str(int_count) + '.tif'
        str_total_path = STR_OUTPUT_DIR + str_file_name

        list_filenames_to_merge.append(str_total_path)

        r = requests.get(i)
        with open(str_total_path, 'wb') as f:
            f.write(r.content)
        int_count += 1
        f.close
        
    # Merge the DEMs in the list_filenames_to_merge
    str_out_tiff_path = STR_OUTPUT_DIR + "AWS_" + str(int_gdf_item) + "_dem_merge.tif"

    d = []
    for file in list_filenames_to_merge:
        src = rasterio.open(file)
        d.append(src)

    out_meta = src.meta.copy()

    mosaic, out_trans = merge(d)

    # Create Metadata of the for the mosaic TIFF
    out_meta.update({"driver": "HFA","height":mosaic.shape[1],"width":mosaic.shape[2],"transform": out_trans,})

    # Write the updated DEM to the specified file path
    with rasterio.open(str_out_tiff_path, "w", **out_meta) as dest:
        dest.write(mosaic)
        dest.close()
        
    # remove the downloaded tiles
    int_count = 0
    for item in d:
        d[int_count].close()
        int_count += 1

    for filename in list_filenames_to_merge:
        if os.path.exists(filename):
            os.remove(filename)
            
    # ************************************************
    # Using RioXarray - translate the DEM back 
    # to the requested shapefile's proj

    src = str_out_tiff_path

    # read the DEM as a "Rioxarray"
    aws_dem = rxr.open_rasterio(src, masked=True).squeeze()

    # reproject the raster to the same projection as the road
    aws_dem_local_proj = aws_dem.rio.reproject(str_crs_boundary)
    aws_dem.close()

    if B_CONVERT_TO_VERT_FT:
        # scale the raster from meters to feet
        aws_dem_local_proj = aws_dem_local_proj * 3.28084

    # clip the raster
    geom_coords = fn_get_features(gdf_boundary_prj, int_gdf_item)
    aws_dem_local_proj_clip = aws_dem_local_proj.rio.clip(geom_coords, from_disk=True)
    aws_dem_local_proj.close()

    # write out the raster
    str_dem_out = STR_OUTPUT_DIR + "AWS_" + str(int_gdf_item) + "_dem_clip_project.tif"
    aws_dem_local_proj_clip.rio.to_raster(str_dem_out,
                                          compress='LZW',
                                          dtype="float32")
    
    aws_dem_local_proj_clip.close()
    # ************************************************
    
    # TODO - 2021.06.07 - is a delay needed to close rioxarray?
    #time.sleep(2)
    
    # remove the unclipped merged file
    #if os.path.exists(str_out_tiff_path):
        #os.remove(str_out_tiff_path)