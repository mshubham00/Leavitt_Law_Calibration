# File: ./leavitt_law/visual.py
####################################################################
import numpy as np
import matplotlib.pyplot as plt
#from mw_plot import MWFaceOn
from lvtlaw.utils import RA_DEC_DIS_to_Galactocentric, save
import pandas as pd                                             #   0
from astropy import units as u
from astropy.coordinates import SkyCoord, ICRS, Galactocentric 
from astropy.coordinates import Latitude, Longitude, Distance
from lvtlaw.utils import img_out_path, mag, ap_bands, abs_bands
import seaborn as sns
sns.set()
bands_label = ap_bands
#####################################################################
def plot_scatter_with_colorbar(x, y, size, color_values, title = ' ', img_path = img_out_path):
    scatter = plt.scatter(x, y, s=size, c=color_values, cmap='viridis', alpha=0.7)
    plt.colorbar(scatter, label='Color Value')
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')
    #plt.xticks(ticks=[])
    plt.title('Scatter Plot with Size and Colorbar')
    if title == ' ':
        pass
    else:
        save(title)
    plt.show()

#####################################################################
def histogram_plot(kind, data, bins=10, title="Histogram", xlabel="Values", ylabel="Frequency", img_path = img_out_path):
    if kind == 1:
        plt.figure(figsize=(8, 6))  # Set the figure size
        plt.hist(data, bins=bins, edgecolor='black', label=data.columns)  # Create the histogram
        plt.legend()
    else:
        data.plot.hist(figsize=(10,6), bins=20, alpha=0.8)      #   4
    plt.title(title)  # Set the title
    plt.xlabel(xlabel)  # Set the x-axis label
    plt.ylabel(ylabel)  # Set the y-axis label
    plt.grid(True, linestyle='--', alpha=0.7)  # Optional: Add gridlines for better readability
    if title == 'Histogram':
        pass
    else:
        save(title,img_path)
    plt.show()
#####################################################################
def cat_photometry(data, xlabel, ylabel, img_path, title='Multiband Photometry'):
    sns.catplot(data)
    plt.title(title)  # Set the title
    plt.xlabel(xlabel)  # Set the x-axis label
    plt.ylabel(ylabel)  # Set the y-axis label
    plt.grid(True, linestyle='--', alpha=0.7)  # Optional: Add gridlines for better readability
    if title == 'Multiband Photometry':
        pass
    else:
        save(title,img_path)
    plt.show()
#####################################################################
def sea_pair(data):
    x = abss
    y = 'logP'
    g = sns.PairGrid(data, x_vars=x, y_vars=y, hue = 'M_V_i')
    g.map_upper(sns.kdeplot)
    g.map_lower(sns.scatterplot)
    g.map_diag(sns.kdeplot)
    g.add_legend()
    plt.show()
#####################################################################
def sea_sub(df):
    fig, axes = plt.subplots(2, 2)
#create boxplot in each subplot
    sns.scatterplot(data=df, x='MB', y='B', ax=axes[0,0])
    sns.scatterplot(data=df, x='B', y='MB', ax=axes[0,1])
    sns.scatterplot(data=df, x='V', y='B', ax=axes[1,0])
    sns.scatterplot(data=df, x='B', y='I', ax=axes[1,1])
    plt.show()
#####################################################################
