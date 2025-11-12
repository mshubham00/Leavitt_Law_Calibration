### File: ./lvtlaw/a_utils.py
'''
a_utils.py contains generic function like regression, save_data, etc. and input/output variables.
'''
module = 'a_utils'
#####################################################################
import os, subprocess, sys
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
from data.datamapping import plots,s,file_name,data_dir,z, image_step, data_out, k, process_step, img_out_path, mag, dis_flag, dis_list, data_cols
img_out_path='./docs/plots/'
#####################################################################
def output_directories(parent_folder = data_out, s=1,subdirectories = process_step):
    if s==1:
        for subdirectory in subdirectories:
            path = os.path.join(parent_folder, subdirectory)
            if not os.path.exists(path):
                os.makedirs(path)
#####################################################################       
def image_directories(parent_folder = img_out_path, plots=1,subdirectories = image_step):
    if plots==1:
        for subdirectory in subdirectories:
            path = os.path.join(parent_folder, subdirectory)
            if not os.path.exists(path):
                os.makedirs(path)
#####################################################################       
def imgsave(title, step=0, img_path=img_out_path, fil = 'pdf', p=1):                                   #   2
    if p == 1:
        print(img_path+image_step[step]+title+'.'+fil)
    plt.savefig('%s%s.%s'%(img_path+image_step[step],title, fil))
#####################################################################
def load_data(data_file = file_name, data_dir = data_dir, mag = mag,  data_cols = data_cols, dis_list = dis_list, p=0):
    data = pd.read_csv(data_dir+data_file+'.csv')
    raw = data[data_cols].dropna().reset_index(drop=True);
    mag = mag
    dis = dis_flag[0]
    if p==1:
        print('\nData Loaded from: \t', data_dir+data_file, '.csv')
        print(f'Distance: {dis} | Bands: {mag}')
        print( data.info())
    return data, raw, mag, dis #, name, ra, dec, EBV, dis
#####################################################################
def regression(x: list, y: list, x_str: str, y_str: str, p = 0):
    regression_line = stats.linregress(x, y); 
    m = regression_line.slope; 
    c = regression_line.intercept
    prediction = m * x + c; 
    residue = y - prediction
    stdd = round(residue.std(ddof=0), 3)
    m_error = regression_line.stderr; 
    c_error = regression_line.intercept_stderr
    if p == 1:
        print(f'{y_str} ( {stdd: .3f} ) = {m:.3f} {x_str} ( {m_error:.3f}) + {c:.3f} ( {c_error : .3f})')
    return m, c, prediction, residue, m_error, c_error, stdd
#####################################################################
def open_output_dir(path):  
    # Open the output folder after process completion
    subprocess.run(['xdg-open', path])
#####################################################################
def colprint(merged_data):
    l = merged_data.columns
    for x in range(0, len(l),40):
        print(l[x:x+40])
#####################################################################
def merge_12(df1, df2, on: list):
    # Ensure `on` is a list
    on = [on] if isinstance(on, str) else on
    overlap = set(df1.columns).intersection(df2.columns) - set(on)
    df2_clean = df2.drop(columns=overlap)
    return df1.merge(df2_clean, on=on)
#####################################################################
def pr_value(x,y,s=0):
    p,r = stats.pearsonr(x,y)
    if s==1:
        print('Pearson R:', r)
        print('P-value:', p)
    return p,r
#####################################################################
'''def RA_DEC_DIS_to_Galactocentric(ra, dec, dis):
    ra = Longitude(ra, unit=u.degree)
    dec = Latitude(dec, unit = u.degree)                        #   1
    dis = 10**(1 + dis/5)/1000          # modulus to kpc
    dis = Distance(dis, unit = u.kpc)
    coordinate = SkyCoord(ra=ra, dec=dec, distance=dis, frame='icrs')
    coordinate = coordinate.transform_to(Galactocentric(galcen_distance=8.1*u.kpc))
    return coordinate'''
#####################################################################
print(f'* * {module} module loaded!')
