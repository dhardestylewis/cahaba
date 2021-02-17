#!/usr/bin/env python3

import geopandas as gpd
import pandas as pd
import numpy as np
import argparse
import sys

input_catchments_fileName = sys.argv[1]
input_flows_fileName = sys.argv[2]
output_catchments_fileName = sys.argv[3]
output_flows_fileName = sys.argv[4]
wbd_fileName = sys.argv[5]
hucCode = str(sys.argv[6])
mask_layer_fileName = sys.argv[7]

input_catchments = gpd.read_file(input_catchments_fileName)
wbd = gpd.read_file(wbd_fileName)
input_flows = gpd.read_file(input_flows_fileName)
mask_layer = gpd.read_file(mask_layer_fileName)

# add -1 meter buffer to mask polygons to avoid masking catchments that only intersect at boundary
mask_layer['geometry'] = mask_layer.buffer(-1)

# must drop leading zeroes
select_flows = tuple(map(str,map(int,wbd[wbd.HUC8.str.contains(hucCode)].fossid)))

if input_flows.HydroID.dtype != 'str': input_flows.HydroID = input_flows.HydroID.astype(str)
output_flows = input_flows[input_flows.HydroID.str.startswith(select_flows)].copy()
if output_flows.HydroID.dtype != 'int': output_flows.HydroID = output_flows.HydroID.astype(int)

if len(output_flows) > 0:
    # merges input flows attributes and filters hydroids
    if input_catchments.HydroID.dtype != 'int': input_catchments.HydroID = input_catchments.HydroID.astype(int)
    output_catchments = input_catchments.merge(output_flows.drop(['geometry'],axis=1),on='HydroID')

    # filter out smaller duplicate features
    duplicateFeatures = np.where(np.bincount(output_catchments['HydroID'])>1)[0]
    # print(duplicateFeatures)

    for dp in duplicateFeatures:
        # print(dp)
        indices_of_duplicate = np.where(output_catchments['HydroID'] == dp)[0]
        # print(indices_of_duplicate)
        areas = output_catchments.iloc[indices_of_duplicate,:].geometry.area
        # print(areas)
        indices_of_smaller_duplicates = indices_of_duplicate[np.where(areas != np.amax(areas))[0]]
        # print(indices_of_smaller_duplicates)
        output_catchments = output_catchments.drop(output_catchments.index[indices_of_smaller_duplicates])

    # remove catchments that overlap with the mask layer (ocean/greatlakes)
    print("removing mask layer...")
    output_catchments = gpd.sjoin(output_catchments, mask_layer, how='left', op='intersects') #options: intersects, within, contains, crosses
    output_catchments = output_catchments.rename(columns={"index_right": "MaskID"}).fillna(-999)
    #output_catchments = output_catchments[output_catchments["mask"] == -999]  # Subset hydroTable to exclude catchments that intersect with mask
    #output_catchments = output_catchments.drop(columns=["mask"])
    print("done removing mask layer...")

    # add geometry column
    output_catchments['areasqkm'] = output_catchments.geometry.area/(1000**2)

    output_catchments.to_file(output_catchments_fileName, driver="GPKG",index=False)
    output_flows.to_file(output_flows_fileName, driver="GPKG", index=False)
