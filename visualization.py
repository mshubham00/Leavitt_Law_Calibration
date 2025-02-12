import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from lvtlaw.utils import colors, data_dir, data_file, data_out, disg, disi, disc, dis_list

df = pd.read_csv(data_dir + data_file)
dfa = pd.read_csv(data_out + '95_abs_data.csv')

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
    fig.suptitle("Period-Luminosity Relation in Multiple Bands")
    
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
plot_period_vs_absolute_magnitude(dfa)

