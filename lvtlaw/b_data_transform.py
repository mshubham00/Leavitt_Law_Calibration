### File: ./lvtlaw/b_data_transform.py
'''
This code converts multiband apparent magnitude and reddening of into extinction, absolute magnitude, true absolute magnitude and wesenheit magnitude in all possible color combinations. The reddening law is adopted from Fouque (2007) derived using Galactic reddening ratio, R_v. The value of reddening ratio taken from a_utils.py   

The output will be saved in 'data/{DatasetName_Rv}/1_prepared/*.csv'

Function contained:
	R123(m,c1,c2): Calculate composite reddening ratio using three bands.
	extinction_law(): Prints the Galactic extinction law as of Table 7 of Fouque 2007.
	extinction(data): Converts reddening into extinction of dataset.
	absolute_magnitude(data): Converts apparent magnitude into absolute magnitude.
	true_absolute_magnitude (absolute_magnitude): Impliment extinction correction on absolute magnitude. 
	reddening_free (absolute_magnitude): Calculate composite wesenheit magnitudes
    transformation(data): calls the above functions and save the results as csv files. 
'''
module = 'b_data_transform'

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
#####################################################################
from data.datamapping import R, A, wes_show, mag, img_out_path, file_name, dis_flag, data_out, dis_list, process_step, k, s, z, R123,p, R_ratio
from lvtlaw.a_utils import merge_12, imgsave
#####################################################################
def extinction_law(A, mag, R):
    print('Adopting BVIJHK Extinction law and reddening ratio from Fouque (2007): \n')
    print ('Bands \t Extinction \t Reddening ratio \n \t A(x)/A(v) \t R(x) for E(B-V)')
    for i in mag:
        print(i,'\t', A[i], '\t \t', R[i], '\n')
    return A, R 

#####################################################################
def wes_deviation(m,wesenheit,n, name, dis, s=0):
    wes_col = {}
    for col in wes_show:
        dev = wesenheit[f'{m}{col}{dis}']-wesenheit[f'{m}{col}{dis}0']
        wes_col[f'{col}'] = dev.std()*10**n
    return wes_col
#####################################################################
def extinction_law_compare(data, plist, precision, s=0):
    fig, axes = plt.subplots(1, 2, figsize=(20, 8), sharey=True)
    axes = axes.flatten()
    heatmaps = []
    data_matrices = []
    for i in range(len(plist)):
        Rv, ex, exlabel = plist[i]
        R, Rv, _ = R_ratio(Rv, mag, ex)
        print(R)
        wes = reddening_free(data, R, mag)
        c = pd.DataFrame()
        for m in mag:
            c[m] = wes_deviation(m, wes, precision, f'{file_name}{exlabel}', dis_flag[0], s=1)
        data_matrices.append(c)
    global_vmin = min(df.min().min() for df in data_matrices)
    global_vmax = max(df.max().max() for df in data_matrices)
    for i, c in enumerate(data_matrices):
        ax = axes[i]
        hm = sns.heatmap(
            c, annot=True, cmap="viridis", ax=ax,
            vmin=global_vmin, vmax=global_vmax, cbar=False
        )
        axes[i].set_title(f"Rv = {plist[i][0]} Ex Law: {plist[i][2]} = {plist[i][1]}")
        heatmaps.append(hm)

    # ---- Add one central colorbar between the two plots ----
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    # Create axis for central colorbar: attached to the right side of axes[0]
    divider = make_axes_locatable(axes[0])
    cax = divider.append_axes("right", size="3%", pad=0.25)

    # Shared colorbar
    fig.colorbar(heatmaps[0].get_children()[0], cax=cax)

    plt.tight_layout()
    if s==1:            
        imgsave('Extinction_compare',img_path=img_out_path)
    plt.show()

#####################################################################
def absolute_magnitude(data, R, mag, dis_flag=dis_flag, dis_list=dis_list, k=k, p=p):
    if p==1:
        print('###'*30)
        print('Absolute magnitude for each band \n')
    absolute = pd.DataFrame({
        'name': data['name'],
        'logP': data['logP'],
        'EBV': data['EBV']})
    for d, dis in enumerate(dis_list):
        absolute[dis] = data[dis]
        for i, m in enumerate(mag):
            if k == 0:  # Madore dataset
                absolute[f'M_{m}{dis_flag[d]}'] = data[f'M_{m}'] + R[m]*data['EBV']
                #else:
                #absolute[f'M_{m}{dis_flag[d]}'] = data[f'{m}_mag'] - data[dis_list[d]]
            elif k ==3 or k == 4:
                absolute[f'M_{m}{dis_flag[d]}'] = data[f'{m}_mag'] #- data[dis_list[d]]
            else:
                absolute[f'M_{m}{dis_flag[d]}'] = data[f'{m}_mag'] - data[dis_list[d]]
    if p==1:
        print(absolute.head())
        print('###' * 30)
    return absolute
#####################################################################
def bandwise_extinction(data, R, mag, p=p):
    if p==1:
        print('Calculated extinction for each band \n')
    #converts reddening into extinction
    extinction = pd.DataFrame({'name': data['name'], 'logP': data['logP'], 'EBV': data['EBV']})
    for i in mag:
        extinction['A_'+i]=data['EBV']*R[i]
    if p ==1:
        print(extinction.head())
        print('###'*30)
    return extinction
#####################################################################
def true_absolute_magnitude(data, R, mag, dis_flag=dis_flag, dis_list=dis_list):
    absolute = absolute_magnitude(data, R, mag)
    extinction = bandwise_extinction(data, R, mag)
    if p==1:
        print(f'True absolute magnitude for each band \n')
    tabsolute = pd.DataFrame({'name': absolute['name'], 'logP': absolute['logP'], 'EBV': absolute['EBV']})
    for d,dis in enumerate(dis_list):
        tabsolute[dis] = absolute[dis]    
        for i,m in enumerate(mag):
                tabsolute[f'M_{m}0{dis_flag[d]}'] = absolute[f'M_{m}{dis_flag[d]}'] - extinction['A_'+m]    
    if p==1:
        print(tabsolute.head())
        print('###'*30) 
    return tabsolute, extinction, absolute
#####################################################################
def reddening_free(data, R, mag, dis_flag=dis_flag, dis_list=dis_list):
    tabsolute, extinction, absolute = true_absolute_magnitude(data, R, mag, dis_flag, dis_list)
    wesen = pd.DataFrame({'name': absolute['name'], 'logP': absolute['logP'], 'EBV': absolute['EBV']})
    #print(R, '\n')
    for d,dis in enumerate(dis_flag):
        wesen[dis_list[d]] = absolute[dis_list[d]]
        for a,c1 in enumerate(mag):
            for b,c2 in enumerate(mag[a+1:]):
                for c,m in enumerate(mag):
                    wes_str = m+c1+c2+dis
                    Rm12 = R123(m,c1,c2, R)
                    #print(f'{wes_str}: {Rm12}', '\n')
                    wesen[wes_str] = absolute[f'M_{m}{dis}'] - Rm12*(absolute[f'M_{c1}{dis}'] - absolute[f'M_{c2}{dis}'])
                    wesen[wes_str+'0'] = tabsolute[f'M_{m}0{dis}']- Rm12*(tabsolute[f'M_{c1}0{dis}']- tabsolute[f'M_{c2}0{dis}'])
                if p==1:
                    print([f'{x+c1+c2}: {R123(x,c1,c2) :.3f}' for x in mag])
    if p==1:
        print(wesen.head())
        print('###'*30)
    return wesen
#####################################################################
def transformation(data, A=A, R=R, mag=mag, dis_flag=dis_flag, dis_list=dis_list, s=s, z=z):
    if p==1:
        extinction_law(A, mag, R) # converts Fouque (2007) extinction law into corresponding reddening ration
        print(' \n Reddening ratio values will be multiplied with E(B-V) values to yield extinction in each band for individual Cepheid along the respective line-of-sight.  \n')
        print('###'*30)
        print('\nApparent magnitude transformed into absolute magnitude and weseheit magnitude using the Galactic extinction law, Reddenings (EBV) and Distance modulus (mu).\n M  = m - mu \n M0 = m - mu - R*EBV \n W  = m - mu - R*(m1-m2) \n')
        print('###'*30)
        print('Apparent magnitude data')
        print(data.head())
    if z==1:
        input('\n')
    tabs_data, ext_data, abs_data = true_absolute_magnitude(data, R, mag)
    if p==1:
        print('Wesenheit magnitude for each band \n')
    wes_data = reddening_free(data, R, mag, dis_flag=dis_flag, dis_list=dis_list)
    merged_data= pd.merge(abs_data, tabs_data, on=['name','logP', 'EBV', f'{dis_list[0]}'])
    merged_data = merge_12(merged_data, wes_data, on = ['name','logP', 'EBV', f'{dis_list[0]}'])
    if s==1:
        data.to_csv(data_out+process_step[0]+file_name +'.csv')
        abs_data.to_csv(data_out+process_step[0]+str(len(abs_data))+ '_abs_data'+'.csv')
        ext_data.to_csv(data_out+process_step[0]+ str(len(ext_data))+ '_ext_data'+'.csv')
        tabs_data.to_csv(data_out+process_step[0]+str(len(tabs_data))+ '_true_abs_data'+'.csv')
        wes_data.to_csv(data_out+process_step[0]+str(len(wes_data))+ '_wes_data'+'.csv')
        merged_data.to_csv(data_out+process_step[0]+str(len(merged_data))+ '_prepared_PLdata'+'.csv')
        print(f'Above data saved in ./{data_out+process_step[0]}\n')
    if z==1:
        input('\n')
    return data, abs_data, ext_data, tabs_data, wes_data, merged_data
#####################################################################
def plot_corr(df, Y='logP', title ='', f=12, s=s):
    sns.set_context("paper", rc={"axes.labelsize": f})
    g = sns.pairplot(data=df, x_vars=df.columns[::], y_vars=Y, kind='scatter')
    g.fig.suptitle(title, fontsize=f)
    g.fig.tight_layout()
    g.fig.subplots_adjust(top=0.9)  # Adjust top to make room for title
    if s == 1:
        imgsave(title,0)    
    plt.show()
#####################################################################
def color_period(data, ann, outliers, s=0):
    color = pd.DataFrame()
    color['name']=data['name']
    color['logP']=data['logP']
    color[dis_list[0]]=data[dis_list[0]]
    color['EBV']=data['EBV']
    for i in range(0,6):
        for j in range(i+1,6):
            color[mag[i]+mag[j]] = data[mag[i]+'_mag'] - data[mag[j]+'_mag'] - (R[mag[i]]-R[mag[j]])*data.EBV
    ls = color.columns[4:]
    for j in range(0,14,2):
        fig, axarr = plt.subplots(1,2, sharey='col',gridspec_kw={'hspace': 0, 'wspace': 0})
        fig = plt.gcf()
        fig.set_size_inches(15, 6)
        Y = color['logP']
        for i,ax in enumerate(axarr):
#        ax.tick_params(left = False, right = False , labelleft = False , labelbottom = False, bottom = False) 
            X = color[ls[i+j]]
            pcm = ax.scatter(X, Y, label='$%s$'%(ls[i+j]), s=color[dis_list[0]], c = color['EBV'])
        #ax.legend(loc='upper right', prop={'size':6})
            ax.yaxis.tick_right()
            if ann == True:
                #for k in range(len(color)):
                for k in outliers:
                    ax.annotate('%i'%(k), xy =(X.iloc[k], Y.iloc[k]), fontsize = 11) 
            if i%2 ==0:
                ax.set_ylabel('Period')
            ax.set_xlabel(ls[i+j])
            plt.text(0.05, 0.85, '%s'%(ls[i+j]), transform = ax.transAxes, color = "red",  fontsize = 14)      
            #ax.set_title(f'Color {ls[i+j]}')
            ax.yaxis.tick_left()
        title = '%s_PC%i_%s'%(file_name,j,ls[i+j])
        if s==1:
            imgsave(title, step=0, img_path=img_out_path, fil = 'pdf', p=1)
#####################################################################
def pltwes_deviation(m,wesenheit,name, dis, s=0):
    fig_res, axs_res = plt.subplots(1, 3, figsize=(18, 4),sharey=True)
    axs_res = axs_res.flatten()
    for col in range(5):
        dev = wesenheit[f'{m}{wes_show[col]}{dis}']-wesenheit[f'{m}{wes_show[col]}{dis}0']
        axs_res[0].axhline(0)#, color='red', linestyle='--', linewidth=1)
        axs_res[0].plot(wesenheit.logP, dev, '.', label =f'{m}{wes_show[col]}{dev.std()*10000 : .3f}4')
        dev = wesenheit[f'{m}{wes_show[col+5]}{dis}']-wesenheit[f'{m}{wes_show[col+5]}{dis}0']
        axs_res[1].axhline(0)#, color='red', linestyle='--', linewidth=1)
        axs_res[1].plot(wesenheit.logP, dev, '.', label =f'{m}{wes_show[col+5]}{dev.std()*10000 : .3f}')
        dev = wesenheit[f'{m}{wes_show[col+10]}{dis}']-wesenheit[f'{m}{wes_show[col+10]}{dis}0']
        axs_res[2].axhline(0)#, color='red', linestyle='--', linewidth=1)
        axs_res[2].plot(wesenheit.logP, dev, '.', label =f'{m}{wes_show[col+10]}{dev.std()*10000 : .3f}')
    axs_res[0].legend()
    axs_res[1].legend()
    axs_res[2].legend()
    axs_res[0].set_ylabel('$W - W_0$')
    axs_res[1].set_xlabel('Period')
    if s==1:
        imgsave(name+m,img_path=img_out_path)
    plt.show()
#####################################################################
def pltwes_deviation_(m,wesenheit,name, dis, s=0):
    fig_res, axs_res = plt.subplots(1, 3, figsize=(18, 4),sharey=True)
    axs_res = axs_res.flatten()
    for col in [0,3]:
        dev = wesenheit[f'{m}{wes_show[col]}{dis}']-wesenheit[f'{m}{wes_show[col]}{dis}0']
        axs_res[0].axhline(0)#, color='red', linestyle='--', linewidth=1)
        axs_res[0].plot(wesenheit.logP, dev, '.', label =m+wes_show[col])
        dev = wesenheit[f'{m}{wes_show[col+1]}{dis}']-wesenheit[f'{m}{wes_show[col+1]}{dis}0']
        axs_res[1].axhline(0)#, color='red', linestyle='--', linewidth=1)
        axs_res[1].plot(wesenheit.logP, dev, '.', label =m+wes_show[col+1])
        dev = wesenheit[f'{m}{wes_show[col+2]}{dis}']-wesenheit[f'{m}{wes_show[col+2]}{dis}0']
        axs_res[2].axhline(0)#, color='red', linestyle='--', linewidth=1)
        axs_res[2].plot(wesenheit.logP, dev, '.', label =m+wes_show[col+2])
    axs_res[0].legend()
    axs_res[1].legend()
    axs_res[2].legend()
    axs_res[0].set_ylabel('$W - W_0$')
    axs_res[1].set_xlabel('Period')
    if s==1:
        imgsave(name+m,img_path=img_out_path)
    plt.show()
#####################################################################
print(f'* * {module} module loaded!')

    
    
    
    
    
    
    
    
    
    
    
    
    

