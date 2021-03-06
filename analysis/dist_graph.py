import numpy as np
import pandas as pd
import matplotlib as plt

df=pd.read_csv("/home/evan/Documents/chicago/ihs/data_median_land_price_psf_CA.csv",sep=",")

sf=df[df['PTYPE2011']=='SINGLE FAMILY']



baseDir="/home/evan/Documents/chicago/dssg-landbank-project/analysis/ca_desc/"
fig = plt.pyplot.figure()
fig.suptitle(CA_names[0],fontsize=14)

subplots_adjust(hspace=0.55)
subplot(111)

sf['land_assmt_11_psf'][sf['CA_name']==CA_names[0]].hist(),
grid(True)
title('Land size and price')
ylabel('count')
xlabel('$')

subplot(222)
sf['bldg_assmt_11_psf'][sf['CA_name']==CA_names[0]].hist()
grid(True)
title('Building size and price')
xlabel('$')


subplot(223)

sf['Msqft_land_11'][sf['CA_name']==CA_names[0]].hist()
grid(True)
ylabel('count')
xlabel('10^3 sf^2')

add_subplot(224)

sf['Msqft_bldg_11'][sf['CA_name']==CA_names[0]].hist()
grid(True)
xlabel('10^3 sf^2')

tight_layout()

figPath=baseDir + CA_names[0] +'.png'
#savefig(figPath)

#clf()
