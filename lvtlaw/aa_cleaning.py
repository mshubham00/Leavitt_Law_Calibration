### File: ./lvtlaw/aa_datacleaning.py
# 1st step
import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path: str):
    """Load data from CSV file"""
    raw_data = pd.read_csv(file_path)
    return raw_data

def select_useful_columns(data: DataFrame, columns: str):
    """Select only the useful columns from the data"""
    return data[columns]

def clean_data(data):
    """Remove incomplete rows and sort data by period"""
    data = data.sort_values(by=['logP'], ascending=True).dropna().reset_index()
    return data

color_cols = ['B_mag', 'V_mag', 'I_mag', 'J_mag', 'H_mag', 'K_mag']

def outliers_from_color_vs_period(data, output_path):
    """Plot color vs period and identify outliers"""
    # Define the color columns (e.g., B-V, V-I, etc.)

    # Create a PDF file to save the plots
    pdf = matplotlib.backends.backend_pdf.PdfPages(f'{output_path}/plots.pdf')

    # Plot color vs period for each color index
    for i in range(0,6):
	for j in (i,6):
	    color_index = data[color_cols[i]] - data[color_cols[j]]
            plt.scatter(data['logP'], data[col])
            plt.xlabel('logP')
            plt.ylabel(col)
            plt.title(f'Color vs Period ({col})')

        # Identify outliers (e.g., using a simple threshold or a more advanced method)
            mean = data[col].mean()
            std = data[col].std()
            outliers = data[(data[col] > mean + 2 * std) | (data[col] < mean - 2 * std)]

        # Annotate the outliers in the plot
            for index, row in outliers.iterrows():
                plt.annotate(f'ID: {row["ID"]}', (row['logP'], row[col]), textcoords="offset points", xytext=(0,10), ha='center')

        # Save the plot to the PDF file
            pdf.savefig(plt.gcf())
            plt.close()

    # Close the PDF file
    pdf.close()

# function for saving plots
def save(title, img_path = './pics/'):
    plt.savefig('%s1%s.pdf'%(img_path,title))

def main(file_path, useful_cols, output_path):
    """Main function to load, clean, and plot the data"""
    raw_data = load_data(file_path)
    data = select_useful_columns(raw_data, useful_cols)
    data = clean_data(data)
    outliers_from_color_vs_period(data, output_path)

if __name__ == '__main__':
    file_path = '../110_RUWE_QLT_Gaia_IRSB.csv'
    useful_cols = ['ID', 'logP', 'mM0_IRSB', 'mMplx', 'EBV', 'B_mag', 'V_mag', 'I_mag', 'J_mag', 'H_mag', 'K_mag', 'DR3Name', 'Gmag', 'BPmag', 'RPmag', 'RA_ICRS', 'DE_ICRS']
    output_path = './data_output'
    main(file_path, useful_cols, output_path)


