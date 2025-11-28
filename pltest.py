from lvtlaw.h_loadoutput import *
from data.datamapping import *
result, r_reg, res, pre = calibrated_result_()
r=r_reg

def print_PL(r, file_name, col):
    slp = r[[f'{m}{col}' for m in mag]].iloc[0]
    inr = r[[f'{m}{col}' for m in mag]].iloc[1]
    esl = r[[f'{m}{col}' for m in mag]].iloc[2]
    ein = r[[f'{m}{col}' for m in mag]].iloc[3]
    stt = r[[f'{m}{col}' for m in mag]].iloc[4]
    print('Leavitt Law', file_name, col)
    for i,m in enumerate(mag):
        #print(f'M_{m}({stt.iloc[i]:.3f}) &= ({slp.iloc[i]:.3f} pm {esl.iloc[i]:.3f})(log P -1) {inr.iloc[i]:.3f} pm {ein.iloc[i]:.3f}\\\\')
    #print(f'M_{m} & = ({slp:.3f} \pm {esl:.3f})(\log P - 1)  {inr:.2f} \pm {ein:.3f} \\\\')
    #print(f"M_{{{m}}} &= ({slp:.3f} \\pm {esl:.3f})(\\log P - 1) {inr:.3f} \\pm {ein:.3f} \\\\")
        print(f'{m}{col} {slp.iloc[i]:.3f} | {stt.iloc[i]:.3f} | {inr.iloc[i]:.3f} ')


for i in wes_show:
    print_PL(r_reg, file_name, f'0')
    print_PL(r_reg, file_name, f'0{i}S')
    
