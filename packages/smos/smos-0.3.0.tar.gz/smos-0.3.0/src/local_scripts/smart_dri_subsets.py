# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

from smos.smos_ic import SMOSDs
from datetime import datetime
from smos.grid import EASE25CellGrid

path = r"R:\Datapool\SMOS\01_raw\datasets\L3_SMOS_IC_Soil_Moisture\DES"

grid_senegal = EASE25CellGrid(bbox= (-17.625, 12.125, -11.125, 16.875))
grid_austria = EASE25CellGrid(bbox= (9.375, 46.375, 17.125, 49.125))
grid_mozambique = EASE25CellGrid(bbox= (30.125, -26.875, 40.875, -10.375))
grid_morocco = EASE25CellGrid(bbox= (-17.125,21.375, -1.125, 35.875))
grid_eu = EASE25CellGrid(bbox=(-11., 34., 43., 71.))

grids = {'Sengal': grid_senegal, 'Austria': grid_austria,
         'Mozambique': grid_mozambique, 'Morocco': grid_morocco}

for country, grid in grids.items():

    ds = SMOSDs(path, grid=grid, read_flags=(0,1))

    ds.write_multiple(r'R:\Projects\SMART-DRI\08_scratch\smos_ic_stacks\DES',
                      start_date=datetime(2010,1,1), end_date=datetime(2018,12,31),
                      stackfile=f'SMOS_IC_DES_{country}_stack.nc')