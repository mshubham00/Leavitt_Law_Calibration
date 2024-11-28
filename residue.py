### File: ./lvtlaw/residue.py
import os
import pandas as pd
import numpy as np
from scipy import stats
from functools import reduce
from lvtlaw.utils import A, R, mag, bands, ap_bands, data_dir, data_file, data_out
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

import os
clear_screen= lambda: os.system('clear')
clear_screen()

data_dir = './data/output/'
regression_file = '102_regression.csv'       # 102 = absolute (1x6), true_absolute (1x6), wesenheint (15x6) 
residue_file = '95_residue.csv'
print(data_dir)

regression_file = pd.read_csv(data_dir+regression_file)
residue_file = pd.read_csv(data_dir+residue_file)
#residue_file.info()
print(residue_file.head(7).T)
def filter_PLW_slope_intercept_data(data = regression_file):
    relations = []
    for i in range(0,17):
        regress_data = data[i*6:6*i+6]
        #print('\n \t %i \t Relation  Slope, intercept, respective error in Gaia (g) and IRSB (i) cases \n '%(i), data[i*6:6*i+6])
        relations.append(regress_data)
    return relations

PLW = filter_PLW_slope_intercept_data()


def filter_residue(data=residue_file):
    relations = []
    for i in range(0,17):
        residue_data = data.T[i*12+3:12*i+15]
        print('\n %i BVIJHK band Residue with Gaia (g) and IRSB (i) cases \n '%(i), residue_data)
        relations.append(residue_data)


residue = filter_residue()


def residue_correlation_Madore(X, Y):
    pass

