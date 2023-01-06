import pandas as pd
import numpy as np
import os

def crtStr(list):
    crtList = []
    for i in list:
        try:
            crt_i = float(i)
        except:
            crt_i = i
        crtList.append(crt_i)
    return(crtList)

file = open('Phase_main_tbl.txt', 'r')
Lines = file.readlines()    

oxide_list = Lines[2].split(' ')[4::]
oxide_list[-1] = oxide_list[-1].split("\n")[0]
end_list = ['phase', 'T_C']

header_liq = ['mass', 'S', 'H', 'V', 'Cp', 'viscosity'] + oxide_list + ['mgno'] + end_list
header_crystal = ['mass', 'S', 'H', 'V', 'Cp', 'formula'] + oxide_list + end_list  #also spinel and oxide
header_cpx = ['mass', 'S', 'H', 'V', 'Cp', 'structure', 'formula'] + oxide_list + end_list
header_wht = ['mass', 'S', 'H', 'V', 'Cp', 'formula'] + end_list
# feldspar_phase = ['mass', 'S', 'H', 'V', 'Cp', 'formula'] + oxide_list

liq_col = []
ol_col = []
sp_col = []
rhm_col = []
cpx_col = []
cpx1_col = []
fsr_col = []
fsr_col1 = []
wht_col = []
t_col = []
p_col = []
for line in Lines:
    if (line != '\n') and ('Title' not in line):
        # print(Lines[0])
        if 'Pressure' in line:
            pressure = float(line.split(' ')[1])
            temperature =float(line.split(' ')[3])
            t_col.append(temperature)
            p_col.append(pressure)
        if 'Pressure' not in line:             
            phase = line.split(' ')[0]
            comp_param = line.split(' ')[1::]
            comp_param[-1] = comp_param[-1].split('\n')[0]
            comp_param = crtStr(comp_param)
            comp_param.append(phase)
            comp_param.append(temperature)
            # comp_param.append(pressure)
            try:
                comp_param.remove('')
            except:
                pass
            if 'olivine' in phase:
                ol_col.append(comp_param)               
            elif 'spinel' in phase:
                sp_col.append(comp_param)
            elif 'clinopyroxene_0' in phase:
                cpx_col.append(comp_param)
            elif 'clinopyroxene_1' in phase:    
                cpx1_col.append(comp_param)
            elif 'feldspar_0' in phase:
                fsr_col.append(comp_param)     
            elif 'feldspar_1' in phase:
                fsr_col1.append(comp_param)               
            elif 'rhm-oxide' in phase:
                rhm_col.append(comp_param)              
            elif 'whitlockite' in phase:
                wht_col.append(comp_param)
            elif 'liquid' in phase:
                liq_col.append(comp_param)


crtMELTS = pd.DataFrame(zip(t_col, p_col), columns=['T_C', 'P_bar']).set_index('T_C')
phase_name = ['liq', 'ol', 'sp', 'cpx', 'cpx1', 'rhm', 'fsr', 'fsr2', 'wht']
data_list = [liq_col, ol_col, sp_col, cpx_col, cpx1_col, rhm_col, fsr_col, fsr_col1, wht_col]
for i, v in enumerate(phase_name):
    if 'cpx' in v:
        df = pd.DataFrame(data_list[i], columns=header_cpx).set_index('T_C')
        df.columns = [x + '_' + v for x in df.columns]
    elif 'wht' in v:
        df = pd.DataFrame(data_list[i], columns=header_wht).set_index('T_C')
        df.columns = [x + '_' + v for x in df.columns]
    elif 'liq' in v:
        df = pd.DataFrame(data_list[i], columns=header_liq).set_index('T_C')
        df.columns = [x + '_' + v for x in df.columns]
    else: 
        df = pd.DataFrame(data_list[i], columns=header_crystal).set_index('T_C')
        df.columns = [x + '_' + v for x in df.columns]

    crtMELTS = crtMELTS.join(df)

crtMELTS.to_excel('crtMELTS.xlsx')