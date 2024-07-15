from __future__ import division
from numpy import array, var
from lmfit import Model, Parameter

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


cluster='A4038'

#######Observed data of A4038############
xd = array([0.029,0.074,0.15,0.24,0.327,0.408,0.606,0.843,1.4])
y_err = array([7,1.5,0.11,0.06,0.15,0.11,0.057,0.03,0.004])
yd = array([42,12.6,5.26,3.04,1.54,0.96,0.427,0.21,0.086])

#########Observed data of A1664########
#xd = array([0.15,0.325,1.4])
#yd = array([1.25,0.45,0.106])
#y_err = array([0.125,0.03,0.04])



	
zd = np.loadtxt(kkfile)[1:,0]
#########insitu model+DM###########

def insituDM(x,scr0,a,vs):
	U=scr0*(x)**(-a)*np.exp(-x**(0.5)/vs**(0.5))
	return U
    			
mod =Model(insituDM)
params = mod.make_params(scr0=1, a=1, vs=1)
params['scr0'].max = 10
params['scr0'].min = 0.01
params['a'].max = 5
params['a'].min = 0.01
params['vs'].max = 5
params['vs'].min = 0.01
result1 = mod.fit(np.abs(yd-zd),params, x=xd, method='leastsq', weights=1+(y_err/yd))
#print(result1.fit_report())	
A=result1.chisqr
L=np.exp(-A**2)
	
##############insitu model#############
def insitu(x,scr0,a,vs):
   	 return scr0*(x)**(-a)*np.exp(-x**(0.5)/vs**(0.5))

mod2 =Model(insitu)
params = mod2.make_params(scr0=1, a=1, vs=1)
params['scr0'].max = 10
params['scr0'].min = 0.01
params['a'].max = 5
params['a'].min = 0.01
params['vs'].max = 5
params['vs'].min = 0.01
result2 = mod2.fit(yd, params,x=xd, method='leastsq', weights=1+(y_err/yd))
#print(result2.fit_report())		
B=result2.chisqr
L1=np.exp(-B**2)

#########plotting##########

TS=-2*np.log(L1/L)

print('-------------------------------')
print('Test Statistic Value   DM likelihood   Null likelihood')
print(TS,L,L1)
print('-------------------------------')
print('Insitu+DM (DM hypothesis)')
print('Parameter    Value       Stderr')
for name, param in result1.params.items():
    	print(f'{name:7s} {param.value:11.5f} {param.stderr:11.5f}')
print('-------------------------------')
print('Insitu (Null hypothesiss)')
print('Parameter    Value       Stderr')
for name, param in result2.params.items():
    	print(f'{name:7s} {param.value:11.5f} {param.stderr:11.5f}')


ci=0.05 * np.std(result1.best_fit) / np.mean(result1.best_fit)
ci1=0.05 * np.std(result2.best_fit) / np.mean(result2.best_fit)


plt.scatter(xd, yd)#, label='Total emission (Jy)')
plt.errorbar(xd, yd,y_err,fmt='.k', ecolor='gray', lw=1)
plt.plot(xd, result1.best_fit, 'r-')#, label='$S_{CR}+S_{\chi}$')
plt.fill_between(xd, (result1.best_fit-ci),(result1.best_fit+ci),color='red', alpha=0.1)
plt.plot(xd, result2.best_fit, 'g--')#, label='$S_{CR}$')
plt.fill_between(xd, (result2.best_fit-ci1),(result2.best_fit+ci1),color='green', alpha=0.1)


plt.xscale('log')
plt.yscale('log')
plt.xlabel("Frequency (Ghz)")
plt.ylabel("Radio Flux (jy)")
#plt.legend()
plt.show()


outfile='TS_%s.out'%cluster
line1=' TS'
latesttable=ww
np.savetxt(outfile,latesttable,'%25.15e', header=line1)














