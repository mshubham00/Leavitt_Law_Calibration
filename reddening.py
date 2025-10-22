import matplotlib.pyplot as plt
from data.datamapping import fouque_extinction_ratios, R_ratio, file_name, wes_show
from lvtlaw.a_utils import imgsave, load_data
from lvtlaw.b_data_transform import transformation
#######################################################################
def plt_wesenheit_deviation(wes_show,A,wesenheit):
    fig_res, axs_res = plt.subplots((int((len(wes_show)-1)/2))+1, 2, figsize=(18, 10))
    axs_res = axs_res.flatten()
    plt.suptitle(f'W{A}')
    for i, col in enumerate(wes_show):
        std_mean = []
        for _,m in enumerate(mag):
            dev = wesenheit[f'{m}{col}_j']-wesenheit[f'{m}{col}_j0']
            axs_res[i].axhline(0)#, color='red', linestyle='--', linewidth=1)
            axs_res[i].plot(wesenheit.logP, dev, '.')
            std_mean.append(dev.std())
        axs_res[i].set_ylabel(f'{col}{sum(std_mean) / len(std_mean):.4f}')
    plt.show()
####################################################################### 
def run_error(n, precision, R_v):
    for i in range(n):
        extinction[err] = fouque_extinction_ratios[err] - i*10**(-precision)
        r, R_v = R_ratio(R_v, mag, A=extinction)
        print(extinction[err])
        _, _, _, _, wesenheit, _  = transformation(raw, R=r, A=extinction, mag=mag)
        plt_wesenheit_deviation(wes_show,extinction,wesenheit)    
####################################################################### 
_, raw, mag, _ = load_data(file_name)
R_v = 3.23
err = 'K'
extinction = fouque_extinction_ratios
#r, R_v = R_ratio(R_v, mag, A=extinction)
#print(r,extinction)
#_, _, _, _, wesenheit, _  = transformation(raw, R=r, A=extinction, mag=mag)
#plt_wesenheit_deviation(wes_show,extinction,wesenheit)
run_error(4, 4, R_v)

####################################################################### 
    
    
    
    
    
