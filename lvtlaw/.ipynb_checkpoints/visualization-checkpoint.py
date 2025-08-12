# File: ./leavitt_law/visualization.py
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from lvtlaw.utils import colors, data_dir, input_data_file, data_out, dis_list, img_out_path, save
from lvtlaw.visual import plot_scatter_with_colorbar

df = pd.read_csv(data_dir + input_data_file)

#dfa = pd.read_csv(data_out + '95_abs_data.csv')




def cordinate(name, ra, dec, EBV, dis, s=0):
    plt.figure(figsize=(10, 6))
    scatter = sns.scatterplot(x=ra, y=dec, hue=EBV, size=dis, sizes=(1, 150), palette="viridis", edgecolor="k")
    cbar = plt.colorbar(scatter.collections[0])
    cbar.set_label("Reddening (EBV)")
    plt.xlabel("Right Ascension (degrees)")
    plt.ylabel("Declination (degrees)")
    plt.title("Galactic Cepheids in the Sky")

    # Annotate some of the points
    for i, row in df.iterrows():
        if i % 12 == 0:  # Label every 10th star for readability
            plt.text(row["RA_ICRS"], row["DE_ICRS"], row["ID"], fontsize=9, ha='right')
    plt.grid(True, linestyle='--', alpha=0.5)

    # Save the plot
    if s == 1:
        output_dir = os.path.join(data_out, "plots")
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, "coordinates.pdf"), format='pdf')
    plt.show()

'''   
def milky_way(ra,dec, dis, title = 'plot_mw', figsize = (8,8),img_path = img_out_path):
    coordinate = RA_DEC_DIS_to_Galactocentric(ra, dec, dis)
    mw1 = MWFaceOn(figsize=figsize,radius=15 * u.kpc, unit=u.kpc, 
        coord="galactocentric", annotation=True,)
    mw1.scatter(-coordinate.x, -coordinate.y, c = 'k', s = 6)
    if title == 'plot_mw':
        pass
    else:
        save(title,img_path)
    plt.axis('off')
    plt.show()
#####################################################################

plt_extinction(ext_data):
    x = 
    y = 
    size =
    color_values = 
    plot_scatter_with_colorbar(x, y, size, color_values)

'''

def plot_corr(df, Y, title='', f=8):
    # To visualize first row of seaborn pairplot
    #plt.figure()
    sns.set_context("paper", rc={"axes.labelsize":f})
    sns.pairplot(data=df, y_vars=df.columns[::], x_vars=Y, kind = 'scatter')
    if title=='':
        pass
    else:
        save(title)
#    plt.title(title)
    plt.show()


def plot_period_vs_magnitude(df):
    bands = ["B_mag", "V_mag", "I_mag", "J_mag", "H_mag", "K_mag"]
    labels = ["B", "V", "I", "J", "H", "K"]
    fig, axes = plt.subplots(nrows=6, ncols=1, figsize=(8, 15), sharex=True)
    
    for ax, band, label in zip(axes, bands, labels):
        scatter = ax.scatter(df["logP"], df[band], c=df["EBV"], cmap="viridis", alpha=0.7, edgecolor="k")
        ax.set_ylabel(f"{label}")
        ax.invert_yaxis()  # Magnitude decreases upwards
        ax.grid(True, linestyle='--', alpha=0.5)
    
    axes[-1].set_xlabel("logP (days)")
    fig.subtitle("Period-Luminosity Relation in Multiple Bands")
    
    # Add colorbar
    cbar = fig.colorbar(scatter, ax=axes, orientation='vertical', label="Reddening (EBV)")
    
    # Save the plot
    output_dir = os.path.join(data_out, "plots")
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, "period_vs_magnitude.pdf"), format='pdf')
    plt.show()



def plot_period_vs_absolute_magnitude(df):
    bands = ["M_B", "M_V", "M_I", "M_J", "M_H", "M_K"]
    labels = ["B", "V", "I", "J", "H", "K"]
    suffixes = ["_i", "_g"]
    colors = ['b', 'y']
    fig, axes = plt.subplots(nrows=6, ncols=1, figsize=(10, 15), sharex=True, sharey=True)    
    for ax, band, label in zip(axes, bands, labels):
        for suffix, color in zip(suffixes, colors):
            band_name = band + suffix
            if band_name in df.columns:
                ax.scatter(df["logP"], df[band_name], c=color, marker = '.', label=f"{label} {suffix}", alpha=0.8)
        ax.set_ylabel(f"{label}")  # Label each subplot with the band name
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.invert_yaxis()  # Magnitude decreases upwards
        ax.legend()
    axes[-1].set_xlabel("logP (days)")
    fig.suptitle("Period-Luminosity Relation in Absolute Magnitudes")
    # Save the plot
    output_dir = os.path.join(data_out, "plots")
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, "period_vs_absolute_magnitude.pdf"), format='pdf')
    plt.show()

# Example usage
#cordinate("Cepheids", df["RA_ICRS"], df["DE_ICRS"], df["EBV"], df["IRSB"], s=1)
#plot_period_vs_magnitude(df)


