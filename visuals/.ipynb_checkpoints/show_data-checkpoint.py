outliers = [0,7,8,67,81,83,85] 
ls = ['BV', 'BI', 'BK', 'VI','VJ','VK','IJ', 'IH', 'IK', 'JH', 'JK', 'HK']
import matplotlib.pyplot as plt
import pandas as pd
import os
import subprocess
import seaborn as sns
img_out_path = '../data/output/9_plots/'
process_step = ['1_datacleaning/','2_PLPW/','3_deldel/', '4_reddening/', '5_dispersion/','6_rms/','7_errorpair/', '8_result/']
raw_data = pd.read_csv('../data/input/cleaned_data.csv')
df = raw_data[["logP", 'IRSB', 'EBV', "B_mag", 'V_mag', 'I_mag', 'J_mag', 'H_mag', 'K_mag']]
data = pd.read_csv('../data/output/1_prepared/95_abs_data.csv')
data = data[["logP", 'plx', 'EBV', "M_B_g", 'M_V_g', 'M_I_g', 'M_J_g', 'M_H_g', 'M_K_g']]

##########################################################################################
def output_directories(parent_folder = img_out_path, s=1,subdirectories = process_step):
    if s==1:
        for subdirectory in subdirectories:
            path = os.path.join(parent_folder, subdirectory)
            if not os.path.exists(path):
                os.makedirs(path)
output_directories(s=1)
##########################################################################################
def savefigure(title, k=0, img_out_path = img_out_path):
    plt.savefig('%s%s%s.pdf'%(img_out_path,process_step[k],title))
##########################################################################################
def plot_corr(df, Y, title='', k=1, f=8):
    # To visualize first row of seaborn pairplot
    #plt.figure()
    sns.set_context("paper", rc={"axes.labelsize":f})
    sns.pairplot(data=df, y_vars=df.columns[::], x_vars=Y, kind = 'scatter')
    if title=='':
        pass
    else:
        savefigure(title, k)
    plt.show()
##########################################################################################
df = pd.read_csv('../data/output/1_prepared/95_wes_data.csv')

bands = ['M_B', 'M_V', 'M_I', 'M_J', 'M_H', 'M_K']
mag = ['B', 'V', 'I', 'J', 'H', 'K']
def plt_wes(w, data, color, title, k=0):
    fig, axarr = plt.subplots(1, 6, sharex='all', sharey='none', gridspec_kw={'hspace': 0, 'wspace': 0})
    fig = plt.gcf()
    fig.set_size_inches(18, 4)  # Adjusting the size for horizontal layout
    d = '_g'
    Y = data['logP']  # LogP is on the x-axis

    # Initialize lists to store all Y and X values for determining common axis limits
    all_X = []
    all_X_wesenheit = []

    for i, ax in enumerate(axarr):
        X = data[bands[i] + d]
        X_wesenheit = w[mag[i] + color + d]

        all_X.extend(X)  # Collecting all X values for later use
        all_X_wesenheit.extend(X_wesenheit)  # Collecting all X_wesenheit values

        ax.scatter(Y, X, label='$%s$' % (bands[i]), s=data['plx'], c=data['EBV'], cmap='viridis')
        ax.scatter(Y, X_wesenheit, label='$%s$' % (bands[i]), s=data['plx'], c='r', marker='+')

        # Add y-axis label specific to the band
        ax.set_ylabel('$W_%s$' % (mag[i]), fontsize=10)

    # Determine common y-axis limits across all subplots
    all_data = all_X + all_X_wesenheit
    y_min = min(all_data)
    y_max = max(all_data)
    
    # Apply common y-axis limits to all subplots and invert the y-axis
    for ax in axarr:
        ax.set_ylim(y_min, y_max)
        ax.invert_yaxis()  # Invert y-axis after setting limits

    # Set common x-axis label and format
    #axarr[2].set_xlabel('Log P with %s' % (color), fontsize=12)

    # Optional: rotate x-axis labels if necessary for better readability
    for ax in axarr:
        ax.tick_params(axis='x', labelrotation=45)

    # Add a color bar for the scatter plot
    cbar = plt.colorbar(axarr[0].collections[0], ax=axarr, orientation='vertical', pad=-0.07, fraction=0.007)
    cbar.set_label('EBV', fontsize=8)

    # Adding a title
    fig.suptitle(title, fontsize=14)
    plt.tight_layout()  # Ensure proper spacing between plots
    savefigure(title, k)
    plt.show()
    return fig  # Return the figure so it can be used later

for i in ['BV', 'VI', 'VK','JK']:
    plt_wes(df, data,i, 'PW_scatter'+i, k=1)
####################################################################################

