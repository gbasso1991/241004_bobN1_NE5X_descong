#%% Analisis para calculo de tau - levantando de archivo resultados.txt y de ciclo
import numpy as np
import matplotlib.pyplot as plt
import fnmatch
import os
import pandas as pd
import chardet 
import re
from glob import glob
from scipy.interpolate import interp1d
from uncertainties import ufloat, unumpy 
#%% LECTOR RESULTADOS
def lector_resultados(path): 
    '''
    Para levantar archivos de resultados con columnas :
    Nombre_archivo	Time_m	Temperatura_(ºC)	Mr_(A/m)	Hc_(kA/m)	Campo_max_(A/m)	Mag_max_(A/m)	f0	mag0	dphi0	SAR_(W/g)	Tau_(s)	N	xi_M_0
    '''
    with open(path, 'rb') as f:
        codificacion = chardet.detect(f.read())['encoding']
        
    # Leer las primeras 6 líneas y crear un diccionario de meta
    meta = {}
    with open(path, 'r', encoding=codificacion) as f:
        for i in range(20):
            line = f.readline()
            if i == 0:
                match = re.search(r'Rango_Temperaturas_=_([-+]?\d+\.\d+)_([-+]?\d+\.\d+)', line)
                if match:
                    key = 'Rango_Temperaturas'
                    value = [float(match.group(1)), float(match.group(2))]
                    meta[key] = value
            else:
                match = re.search(r'(.+)_=_([-+]?\d+\.\d+)', line)
                if match:
                    key = match.group(1)[2:]
                    value = float(match.group(2))
                    meta[key] = value
                else:
                    # Capturar los casos con nombres de archivo en las últimas dos líneas
                    match_files = re.search(r'(.+)_=_([a-zA-Z0-9._]+\.txt)', line)
                    if match_files:
                        key = match_files.group(1)[2:]  # Obtener el nombre de la clave sin '# '
                        value = match_files.group(2)     # Obtener el nombre del archivo
                        meta[key] = value
                    
    # Leer los datos del archivo
    data = pd.read_table(path, header=18,
                         names=('name', 'Time_m', 'Temperatura',
                                'Remanencia', 'Coercitividad','Campo_max','Mag_max',
                                'frec_fund','mag_fund','dphi_fem',
                                'SAR','tau',
                                'N','xi_M_0'),
                         usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13),
                         decimal='.',
                         engine='python',
                         encoding=codificacion)
        
    files = pd.Series(data['name'][:]).to_numpy(dtype=str)
    time = pd.Series(data['Time_m'][:]).to_numpy(dtype=float)
    temperatura = pd.Series(data['Temperatura'][:]).to_numpy(dtype=float)
    Mr = pd.Series(data['Remanencia'][:]).to_numpy(dtype=float)
    Hc = pd.Series(data['Coercitividad'][:]).to_numpy(dtype=float)
    campo_max = pd.Series(data['Campo_max'][:]).to_numpy(dtype=float)
    mag_max = pd.Series(data['Mag_max'][:]).to_numpy(dtype=float)
    xi_M_0=  pd.Series(data['xi_M_0'][:]).to_numpy(dtype=float)
    SAR = pd.Series(data['SAR'][:]).to_numpy(dtype=float)
    tau = pd.Series(data['tau'][:]).to_numpy(dtype=float)
   
    frecuencia_fund = pd.Series(data['frec_fund'][:]).to_numpy(dtype=float)
    dphi_fem = pd.Series(data['dphi_fem'][:]).to_numpy(dtype=float)
    magnitud_fund = pd.Series(data['mag_fund'][:]).to_numpy(dtype=float)
    
    N=pd.Series(data['N'][:]).to_numpy(dtype=int)
    return meta, files, time,temperatura,  Mr, Hc, campo_max, mag_max, xi_M_0, frecuencia_fund, magnitud_fund , dphi_fem, SAR, tau, N



#%% 265 57
resultados_265 = glob(os.path.join('./265_57', '**', '*resultados.txt'),recursive=True)

meta_1,files_1,time_1,temperatura_0_1,Mr_1,Hc_1,campo_max_1,mag_max_1,xi_M_0_1,frecuencia_fund_1,magnitud_fund_0_1,dphi_fem_0_1,SAR_0_1,tau_0_1,N1 = lector_resultados(resultados_265[0])
meta_2,files_2,time_2,temperatura_0_2,Mr_2,Hc_2,campo_max_2,mag_max_2,xi_M_0_2,frecuencia_fund_2,magnitud_fund_0_2,dphi_fem_0_2,SAR_0_2,tau_0_2,N2 = lector_resultados(resultados_265[1])
meta_3,files_3,time_3,temperatura_0_3,Mr_3,Hc_3,campo_max_3,mag_max_3,xi_M_0_3,frecuencia_fund_3,magnitud_fund_0_3,dphi_fem_0_3,SAR_0_3,tau_0_3,N3 = lector_resultados(resultados_265[2])
# meta_4,files_4,time_4,temperatura_0_4,Mr_4,Hc_4,campo_max_4,mag_max_4,xi_M_0_4,frecuencia_fund_4,magnitud_fund_0_4,dphi_fem_0_4,SAR_0_4,tau_0_4,N3 = lector_resultados(resultados_265[3])

#%% Tau vs Temp
fig,((ax,ax2),(ax3,ax4))= plt.subplots(nrows=2,ncols=2,figsize=(12,8),constrained_layout=True,sharex=True)

ax.plot(temperatura_0_1,tau_0_1,'.-',label='1')
ax.plot(temperatura_0_2,tau_0_2,'.-',label='2')
ax.plot(temperatura_0_3,tau_0_3,'.-',label='3')
#ax.plot(temperatura_0_4,tau_0_4,'.-',label='4')
ax.set_title(r'$\tau$')
ax.set_ylabel(r'$\tau$ (s)')

ax2.plot(temperatura_0_1,SAR_0_1,'.-',label='1')
ax2.plot(temperatura_0_2,SAR_0_2,'.-',label='2')
ax2.plot(temperatura_0_3,SAR_0_3,'.-',label='3')
#ax2.plot(temperatura_0_4,SAR_0_4,'.-',label='4')
ax2.set_title('SAR')
ax2.set_ylabel('SAR (W/g)')

ax3.plot(temperatura_0_1,Mr_1,'.-',label='1')
ax3.plot(temperatura_0_2,Mr_2,'.-',label='2')
ax3.plot(temperatura_0_3,Mr_3,'.-',label='3')
#ax3.plot(temperatura_0_4,Mr_4,'.-',label='4')
ax3.set_title('M$_R$')
ax3.set_ylabel('M$_R$ (A/m)')

ax4.plot(temperatura_0_1,Hc_1,'.-',label='1')
ax4.plot(temperatura_0_2,Hc_2,'.-',label='2')
ax4.plot(temperatura_0_3,Hc_3,'.-',label='3')
#ax4.plot(temperatura_0_4,Hc_4,'.-',label='4')
ax4.set_title('H$_C$')
ax4.set_ylabel('H$_C$  (kA/m)')


for a in [ax,ax2,ax3,ax4]:
    a.legend()
    a.grid()
    
ax3.set_xlabel('T (°C)')
ax4.set_xlabel('T (°C)')
plt.suptitle('Comparativa - NE5X\n265 kHz 57 kA/m')
plt.savefig('265_57_NE5X_comparativa.png',dpi=300)
plt.show()
#%%
#SAR vs Temp
fig2,ax= plt.subplots(figsize=(9,5),constrained_layout=True)

plt.legend()
plt.grid()
plt.ylabel('SAR (W/g)')
plt.xlabel('T (°C)')
plt.title(r'SAR - '+ identif_0)
plt.savefig('SAR_vs_T_'+identif_0+'.png',dpi=300)
plt.show()

# H coercitivo vs Temp
fig3,ax= plt.subplots(figsize=(9,5),constrained_layout=True)
ax.plot(temperatura_0_1,Hc_1,'.-',label='1')
ax.plot(temperatura_0_2,Hc_2,'.-',label='2')
ax.plot(temperatura_0_3,Hc_3,'.-',label='3')
ax.plot(temperatura_0_4,Hc_4,'.-',label='4')
plt.legend()
plt.grid()
plt.ylabel('H$_C$  (kA/m)')
plt.xlabel('T (°C)')
plt.title('H$_C$ - '+ identif_0)
plt.savefig('Hc_vs_T_'+identif_0+'.png',dpi=300)
plt.show()

# M remanente vs Temp
fig4,ax= plt.subplots(figsize=(9,5),constrained_layout=True)
ax.plot(temperatura_0_1,Mr_1,'.-',label='1')
ax.plot(temperatura_0_2,Mr_2,'.-',label='2')
ax.plot(temperatura_0_3,Mr_3,'.-',label='3')
ax.plot(temperatura_0_4,Mr_4,'.-',label='4')
plt.legend()
plt.grid()
plt.ylabel('M$_R$ (A/m)')
plt.xlabel('T (°C)')
plt.title('M$_R$  - '+ identif_0)
plt.savefig('Mr_vs_T_'+identif_0+'.png',dpi=300)
plt.show()

#%%
#%% tiempos a tiempos absolutos y hago coiu
t_1=time_1-time_1[0]
t_2=time_2-time_2[0]
t_3=time_3-time_3[0]

#Tau vs time
fig,ax= plt.subplots(figsize=(9,5),constrained_layout=True)
ax.plot(time_1,tau_0_1,'.-',label='1')
ax.plot(time_2,tau_0_2,'.-',label='2')
ax.plot(time_3,tau_0_3,'.-',label='3')
plt.legend()
plt.grid()
plt.ylabel(r'$\tau$ (s)')
plt.xlabel('time (s)')
plt.title(r'$\tau$ - '+ identif_0)
#plt.savefig('tau_vs_time_'+identif_0+'.png',dpi=300)
plt.show()

#SAR vs Temp
fig2,ax= plt.subplots(figsize=(9,5),constrained_layout=True)
ax.plot(time_1,SAR_0_1,'.-',label='1')
ax.plot(time_2,SAR_0_2,'.-',label='2')
ax.plot(time_3,SAR_0_3,'.-',label='3')
plt.legend()
plt.grid()
plt.ylabel('SAR (W/g)')
plt.xlabel('time (s)')
plt.title(r'SAR - '+ identif_0)
#plt.savefig('SAR_vs_time_'+identif_0+'.png',dpi=300)
plt.show()

# H coercitivo vs Temp
fig3,ax= plt.subplots(figsize=(9,5),constrained_layout=True)
ax.plot(time_1,Hc_1,'.-',label='1')
ax.plot(time_2,Hc_2,'.-',label='2')
ax.plot(time_3,Hc_3,'.-',label='3')
plt.legend()
plt.grid()
plt.ylabel('H$_C$  (kA/m)')
plt.xlabel('time (s)')
plt.title('H$_C$ - '+ identif_0)
#plt.savefig('Hc_vs_time_'+identif_0+'.png',dpi=300)
plt.show()

# M remanente vs Temp
fig4,ax= plt.subplots(figsize=(9,5),constrained_layout=True)
ax.plot(time_1,Mr_1,'.-',label='1')
ax.plot(time_2,Mr_2,'.-',label='2')
ax.plot(time_3,Mr_3,'.-',label='3')
plt.legend()
plt.grid()
plt.ylabel('M$_R$ (A/m)')
plt.xlabel('time (s)')
plt.title('M$_R$  - '+ identif_0)
#plt.savefig('Mr_vs_time_'+identif_0+'.png',dpi=300)
plt.show()




