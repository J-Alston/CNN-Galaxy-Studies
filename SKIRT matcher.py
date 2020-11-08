# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 14:43:48 2020

@author: Jack
"""
import numpy as np
import matplotlib.pyplot as plt
import os
from astropy.io import fits
plt.style.use('classic')

#read data
assembly_data = np.loadtxt(r'C:\Users\Jack\Documents\Uni\Year 4\Project\data\stellar assembly data\assembly data.csv')
#file strucutre is [isd, esd, total]
SKIRT_fnames = os.listdir(r'C:\Users\Jack\Documents\Uni\Year 4\Project\data\sdss_099\sdss\snapnum_099\data')[:-1]
assembly_data = np.transpose(assembly_data)

#get image IDs which correspond to positions in stellar assembly arrays
index_array = []
for i in SKIRT_fnames:
    counter = 0
    while i[counter] != '.':
        counter += 1
    index_array.append(int(i[10:counter]))

#get stellar assembly info for SKIRT images using IDs found above
SKIRT_assembly_data = [assembly_data[i] for i in index_array]
SKIRT_assembly_data = np.transpose(SKIRT_assembly_data)
SKIRT_assembly_data = np.transpose(np.array([SKIRT_assembly_data[0], SKIRT_assembly_data[1], SKIRT_assembly_data[2], index_array]))
ESMF = [i[1]/i[2] for i in SKIRT_assembly_data]
ISMF = [i[0]/i[2] for i in SKIRT_assembly_data]
total = [i[2] for i in SKIRT_assembly_data]
ID = [i[3] for i in SKIRT_assembly_data]

#plot selection of images based on limits selected by user
#this code also displays the objects' ESMFs and total masses

def image_plotter(ESMF_Range, Total_Range, path):
    
    cut_ESMF = [ESMF[i] for i in range(len(ESMF)) if Total_Range[0] < total[i] < Total_Range[1] and ESMF_Range[0] < ESMF[i] < ESMF_Range[1]]
    cut_total = [total[i] for i in range(len(ESMF)) if Total_Range[0] < total[i] < Total_Range[1] and ESMF_Range[0] < ESMF[i] < ESMF_Range[1]]
    cut_ID = [ID[i] for i in range(len(ESMF)) if Total_Range[0] < total[i] < Total_Range[1] and ESMF_Range[0] < ESMF[i] < ESMF_Range[1]]
    fnames = [path + r'\broadband_' + str(int(i)) + '.fits' for i in cut_ID]
    
    print(f'There are {len(fnames)} objects in this sample. Type how many you would like to display.')
    lim = int(input())
    
    cut_ESMF, cut_total, cut_ID = cut_ESMF[0:lim], cut_total[0:lim], cut_ID[0:lim]
    
    if np.sqrt(len(cut_ID))%1 != 0:
        fig_side_length = int(np.sqrt(len(cut_ID)))+1
    if np.sqrt(len(cut_ID))%1 == 0.0:
        fig_side_length = int(np.sqrt(len(cut_ID)))
    
    fig = plt.figure(figsize=[5*fig_side_length, 5*fig_side_length])
    ax = fig.subplots(fig_side_length, fig_side_length)
    
    for i in range(fig_side_length):
        counter = 0
        while counter < fig_side_length:
            if i*fig_side_length+counter < len(cut_ID):
                hdul = fits.open(fnames[i*fig_side_length+counter])
                print(i,i*fig_side_length+counter)
                ax[i][counter].imshow(np.arcsinh(hdul[0].data[0]), cmap = 'gray')
                ax[i][counter].set_title('ESMF = ' + str(np.round(cut_ESMF[i*fig_side_length+counter], 4))+' Total Mass = ' + str(np.round(cut_total[i*fig_side_length+counter],4)))
                counter +=1
            else:
                counter += 1

#just some example runs
image_plotter([0,0.01], [0, 1000], r'C:\Users\Jack\Documents\Uni\Year 4\Project\data\sdss_099\sdss\snapnum_099\data')
image_plotter([0.9,1], [0, 1000], r'C:\Users\Jack\Documents\Uni\Year 4\Project\data\sdss_099\sdss\snapnum_099\data')
    