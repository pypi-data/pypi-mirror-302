# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -
from smos import SMOSTs
import pandas as pd
import matplotlib.pyplot as plt

path_old = r'R:\Datapool\SMOS\02_processed\L3_SMOS_IC_Soil_Moisture\timeseries\ASC'
path_new = r"\\project10\data-write\USERS\wpreimes\smosic_ts\asc"

ds_new = SMOSTs(path_new, parameters=['Soil_Moisture'])
ds_old = SMOSTs(path_old, parameters=['Soil_Moisture'])

ts_old = ds_old.read(-14,14).rename(columns={'Soil_Moisture': 'old_sm'})
ts_new = ds_new.read(-14,14).rename(columns={'Soil_Moisture': 'new_sm'})

df = pd.concat([ts_old, ts_new+0.1], axis=1)
df.plot(marker='.')
plt.show()