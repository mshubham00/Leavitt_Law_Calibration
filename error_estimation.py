### File: ./lvtlaw/error_estimation.py

from lvtlaw.utils import colors,data_dir, data_file, data_out, R, mag
import pandas as pd
from lvtlaw.pl_pw import pl_reg     #pl_reg(data,'_g','_i') -> PLW, residue, prediction
from lvtlaw.data_transform import transformation, extinction_law

res = pd.read_csv(data_out+'95_del_res.csv')
res_M = pd.read_csv(data_out+'95_del_res_M.csv')

del_slope = pd.read_csv(data_out+'95_del_slope_intercept.csv')
del_slope_M = pd.read_csv(data_out+'95_del_slope_intercept_M.csv')

print(res.head(), '\n',res_M.head())
print(del_slope.head(),'\n', del_slope_M.head())

def calculate_extinction_reddening(name = res.name, del_W, del_M, slope):
    del_mu = [i*0.01 for i in range(-100,100,2)]
    extinction = pd.DataFrame()
    extinction['name']=name
    for mu in del_mu:
        extinction['%f'%(mu)] = (del_M + mu) - slope*(del_W + mu)
    return del_mu, extinction

def calculate_reddening_error(name, del_mu, extinction_bands, R, mag)
    reddening = pd.DataFrame()
    reddening['name'] = name
    for i in range(0,6):
        reddening[mag[i]] = extinction_bands[mag[i]]/R[i]
    return reddening

result_color = []
for col in colors:
    wes_result = []
    for i in range(0,6):
        wes = mag[i] + col
        del_W = res['r_'+wes]
        del_M = res['r_'+mag[i]]
        slope = del_slope[mag[i]+wes] 
        del_mu, extinction = calculate_extinction_reddening(name, del_W, del_M, slope)
        wes_result.append(extinction)
    result_color.append(wes_result)


def find_rms(name, reddening, del_mu):
    dispersion_over_mu = []
    average_over_mu = []
    for mu in del_mu:
        averageg=sum(reddening[0:6]) / len(reddening_errorg[0:6])
        rmsg = sum((reddening_errorg[0:6]-averageg)**2)**0.5
        dispersion_over_mug.append(rmsg)#[0]
        average_over_mug.append(averageg)
        averagei=sum(reddening_errori[0:6]) / len(reddening_errori[0:6])
        rmsi = sum((reddening_errori[0:6]-averagei)**2)**0.5
        dispersion_over_mui.append(rmsi)#[0]
        average_over_mui.append(averagei)
    min_indexg = dispersion_over_mug.index(min(dispersion_over_mug))
    min_indexi = dispersion_over_mui.index(min(dispersion_over_mui))
    E_valueg=average_over_mug[min_indexg]
    mu_valueg = mug[min_indexg]
    E_valuei=average_over_mui[min_indexi]
    mu_valuei = mug[min_indexi]


='VI'
wesen = 'VVI'
y=[]
extinctiong = []
reddeningg = []
extinctioni = []
reddeningi = []
for i in range(0,6):
    exg,redg,mu_str, mug = calculate_extinction_reddening('r_'+mag[i]+col+disg, 'r_'+mag[i]+disg, mag[i]+wesen,R[i])
    extinctiong.append(exg)
    reddeningg.append(redg)
    exi,redi,mu_str, mui = calculate_extinction_reddening('r_'+mag[i]+col+disi, 'r_'+mag[i]+disg, mag[i]+wesen,R[i])
    extinctioni.append(exi)
    reddeningi.append(redi)



def star_error(star):
    dispersion_over_mug = []
    average_over_mug = []
    dispersion_over_mui = []
    average_over_mui = []
    for str_mu in mu_str:
        reddening_errorg=[]
        reddening_errori=[]
        for j in range(0,6):
            reddening_errorg.append(reddeningg[j][str_mu].iloc[star])
            reddening_errori.append(reddeningi[j][str_mu].iloc[star])
        averageg=sum(reddening_errorg[0:6]) / len(reddening_errorg[0:6])
        rmsg = sum((reddening_errorg[0:6]-averageg)**2)**0.5
        dispersion_over_mug.append(rmsg)#[0]
        average_over_mug.append(averageg)
        averagei=sum(reddening_errori[0:6]) / len(reddening_errori[0:6])
        rmsi = sum((reddening_errori[0:6]-averagei)**2)**0.5
        dispersion_over_mui.append(rmsi)#[0]
        average_over_mui.append(averagei)
    min_indexg = dispersion_over_mug.index(min(dispersion_over_mug))
    min_indexi = dispersion_over_mui.index(min(dispersion_over_mui))
    E_valueg=average_over_mug[min_indexg]
    mu_valueg = mug[min_indexg]
    E_valuei=average_over_mui[min_indexi]
    mu_valuei = mug[min_indexi]
    return mu_valueg, E_valueg, dispersion_over_mug , min_indexg, mu_valuei, E_valuei, dispersion_over_mui , min_indexi
#mu_correction.append(mu_value)


for star in range(0,cepheid):
    x,y, z, w = star_error(star)
    for i in range(0,6):
        plt.plot(mug,reddeningg[i].iloc[star][1:], label = mag[i])
    plt.plot(mug, z, 'k.')
#    plt.plot(x,y,'o')
    plt.annotate(data.name.iloc[star],(0,0))
    plt.legend()
    save('stars/%i%s'%(star,data.name.iloc[star]))
    plt.show()


mu_errorg = []
E_errorg = []
indexg=[]
mu_errori = []
E_errori = []
indexi=[]
for star in range(0,cepheid):
    xg,yg,zg, wg, xi,yi,zi, wi=star_error(star)
    mu_errorg.append(xg)
    E_errorg.append(yg)
    indexg.append(wg)
    mu_errori.append(xi)
    E_errori.append(yi)
    indexi.append(wi)

correctiong=pd.DataFrame(columns=['mu']+mag)
correctioni=pd.DataFrame(columns=['mu']+mag)
for star in range(0,cepheid):
    lsg=[]
    lsi=[]
    lsg.append(float(mug[indexg[star]]))
    lsi.append(float(mui[indexi[star]]))
    for i in range(0,6):
        lsg.append(extinctiong[i][mu_str[indexg[star]]].iloc[star])
        lsi.append(extinctioni[i][mu_str[indexi[star]]].iloc[star])
    correctiong.loc[len(correctiong)]=lsg
    correctioni.loc[len(correctioni)]=lsi
correctiong['name']=data.name
correctioni['name']=data.name
#correction.to_csv('./%i_correction_IRSB.csv'%(len(correction)))#.info()



new_modg = data['mod_g']+mu_errorg
new_redg = data['EBV'] + E_errorg
new_modi = data['mod_i']+mu_errori
new_redi = data['EBV'] + E_errori



