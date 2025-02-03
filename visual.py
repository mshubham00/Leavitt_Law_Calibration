# File: ./leavitt_law/visual.py
####################################################################
import numpy as np
import matplotlib.pyplot as plt
from mw_plot import MWFaceOn
import pandas as pd                                             #   0
from astropy import units as u
from astropy.coordinates import SkyCoord, ICRS, Galactocentric 
from astropy.coordinates import Latitude, Longitude, Distance
from lvtlaw.utils import img_out_path, mag, bands_label, abs_bands
import seaborn as sns
sns.set()
#####################################################################
def RA_DEC_DIS_to_Galactocentric(ra, dec, dis):
    ra = Longitude(ra, unit=u.degree)
    dec = Latitude(dec, unit = u.degree)                        #   1
    dis = 10**(1 + dis/5)/1000          # modulus to kpc
    dis = Distance(dis, unit = u.kpc)
    coordinate = SkyCoord(ra=ra, dec=dec, distance=dis, frame='icrs')
    coordinate = coordinate.transform_to(Galactocentric(galcen_distance=8.1*u.kpc))
    return coordinate
#####################################################################
def save(title, img_path):                                      #   2
    plt.savefig('%s2%s.pdf'%(img_path,title))
#####################################################################
def milky_way(ra,dec, dis, figsize = (8,8), title = 'plot_mw', img_path = './'):
    coordinate = RA_DEC_DIS_to_Galactocentric(ra, dec, dis)
    mw1 = MWFaceOn(figsize=figsize,radius=15 * u.kpc, unit=u.kpc, 
        coord="galactocentric", annotation=True,)
    mw1.title = "Spread of observed Cepheid stars around the Sun"#  3
    mw1.scatter(-coordinate.x, -coordinate.y, c = 'r', s = 6)
    if title == 'plot_mw':
        pass
    else:
        save(title,img_path)
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



data = pd.read_csv('./data/input/cleaned_data.csv')             
data_abs = pd.read_csv('./data/output/95_abs_data.csv')             
data_ = data[['plx', 'IRSB']]
data_E= data[['EBV', 'logP']]
data_m = data[bands_label] #- data['plx']
abss = []
tick_true = []
tick_abs = []
data_M = pd.DataFrame()
for i in range(0,6):
    abss.append(abs_bands[i] + '_i')
    tick_true.append(mag[i]+'0')
    tick_abs.append('M'+mag[i])
    data_M[abs_bands[i]] = data[bands_label[i]] - data['IRSB']
data_M0 = pd.DataFrame()
#data_M0['logP'] = data['logP']
#data_M0['IRSB'] = data['IRSB']
data_M0[mag] = data[bands_label]
data_M0[tick_abs] = data_M[abs_bands]
data_M0[tick_true] = data_abs[abss]
print(data_M0.info())
output_path = './data/output/plots/'
dis = data.IRSB #* u.kpc
ra = data.RA_ICRS                                               #   4
dec = data.DE_ICRS
##################################################################### 
#milky_way(ra,dec,dis, title = 'milkyway', img_path=output_path)

#histogram_plot(kind = 1, data = data_, bins=20, title='IRSB vs Parallax Distance', xlabel='Distance Range (in modulus)', ylabel='Number of Cepheid stars')
#histogram_plot(kind = 2, data = data_, bins=20, title='IRSB vs Parallax Distance', xlabel='Distance Range (in modulus)', ylabel='Number of Cepheid stars')
sea_sub(data_M0)
#histogram_plot(kind = 1, data = data_E, bins=20, title='Period and Reddening Distribution', xlabel='Values', ylabel='Number of Cepheid stars')
#sea_pair(data_M0)
#photometry(data_M, title = 'apparent',xlabel = 'Luminosity in magnitude unit', ylabel = 'Number of Cepheids', img_path=img_out_path)
#cat_photometry(data_M0,  title = 'Comparision',xlabel = 'Luminosity in magnitude unit', ylabel = 'Number of Cepheids', img_path=img_out_path)
#photometry(data_M0,  title = 'true_absolute',xlabel = 'Luminosity in magnitude unit', ylabel = 'Number of Cepheids', img_path=img_out_path)
