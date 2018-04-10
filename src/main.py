import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
import os

from src import redshiftFinder
color = ['red', 'green', 'black', '#783BA1', '#FFAA1D', '#FA02F2', '#B8B48A']

#Finding SNR
def findSNR(obs_data):
    obs_data[:,2]=1/obs_data[:,2]
    #print(obs_data)
    return  obs_data


#Loading observation spectra file
def load_ObservationData(filePath):
     obs_data=np.loadtxt('/Users/sumithkuttiyilsuresh/PycharmProjects/FindRedshifts/data/J10513545.txt')
     return obs_data


#Loading absorption line file
def load_AbsorptionSpectrum(filePath):
    #print(filePath)
    absSpectra_file = np.array(pd.read_excel('/Users/sumithkuttiyilsuresh/PycharmProjects/FindRedshifts/data/newIonList.xlsx'))
    return absSpectra_file

#Find out the local minimas in the plot
def find_localMinimas(obs_data):
    localminima_data=[]
    maxInd = argrelextrema(np.asarray(obs_data[:,1]), np.less, order=3)
    localminima_data=obs_data[maxInd]
    localminima_data=np.array(localminima_data)
    return localminima_data

#Plot the observation data
def plot_graph(obs_data, localminima_data):
    #plt.xlim(np.min(obs_data[:, 0])+300, np.max(obs_data[:, 0])+300)
    #plt.ylim(np.min(obs_data[:, 1])+0.2, np.max(obs_data[:, 1])+0.2)
    plt.xlim(np.min(obs_data[:, 0]), np.max(obs_data[:, 0]))
    plt.ylim(np.min(obs_data[:, 1]), np.max(obs_data[:, 1]))
    plt.plot(obs_data[:, 0], obs_data[:, 1])


    threshold_flux=np.average(localminima_data[:, 1])-0.04
    #print('Threshold value :-', threshold_flux)
    return plt

def plot_minima_in_graph(obs_data, localminima_data, color):
    #localminima_data = localminima_data[np.logical_not(localminima_data[:, 1] > threshold_flux)]
    rest_wavelength=''
    common_flux_loc=0
    common_wav_loc=0
    for i in range(0, np.shape(localminima_data)[0]):
        if(rest_wavelength==localminima_data[i][2]):
          plt.annotate(str(localminima_data[i][3])+"("+(str(localminima_data[i][2])+")"),

                     xy=(localminima_data[i][0], localminima_data[i][1]),
                     xytext=(common_wav_loc, common_flux_loc),
                     color=color,
                     rotation=-90, arrowprops=dict(arrowstyle="->", color=color))

        else:
            plt.annotate(str(localminima_data[i][3]) + "(" + (str(localminima_data[i][2]) + ")"),
                         xy=(localminima_data[i][0], localminima_data[i][1]),
                         xytext=(localminima_data[i][0], np.max(obs_data[:, 1])-0.1),

                         color=color,
                         rotation=-90, arrowprops=dict(arrowstyle="->", color=color))
            common_flux_loc = np.max(obs_data[:, 1]) - 0.1
            common_wav_loc = localminima_data[i][0]
        rest_wavelength=localminima_data[i][2]



def annotateGraph(plt, discovered_z, number_of_points):
    red_patch=[]
    count=0
    for z in discovered_z:
        red_patch.append(mpatches.Patch(color=color[count], label=r'$Z_{system%i}=%0.4f\pm%0.4f$(%i)'%(count+1,round(z[0],4),round(z[1],4),number_of_points[count])))
        count+=1
    plt.legend(handles=red_patch, loc='lower right')




def mainMethod(number_of_system):
    #####################start##########################
    threshold_flux = -0.2
    print(number_of_system)


    redShiftrange = [1, 5.3]
    # nspec_0394_403_51913.dat
    # spec_0394_264_51913.dat
    # quasar_1.txt
    # quasar_2.txt
    # OI1302p2.txt
    # q1323_sdssspec.dat
    abs_data = load_AbsorptionSpectrum('data/newIonList.xlsx')
    # abs_data=load_AbsorptionSpectrum('data/ion_to_search_1.xlsx')
    # J1051+3545.txt
    # obs_data=load_ObservationData('data/nspec_0394_403_51913.dat')
    # obs_data=load_ObservationData('data/nspec_0394_264_51913.dat')
    obs_data = load_ObservationData('data/quasar_1.txt')  # q1224
    # obs_data=load_ObservationData('data/quasar_2.txt')#q1009
    # obs_data=load_ObservationData('data/OI1302p2.txt')
    # obs_data=load_ObservationData('data/q1323_sdssspec.dat')
    # obs_data=load_ObservationData('data/J1051+3545.txt')

    # obs_data=load_ObservationData('data/J10513545.txt')
    obs_data = findSNR(obs_data)

    # print(obs_data)
    # obs_data=redshiftFinder.addError(obs_data)
    # print(obs_data[0])
    #####################end############################
    obs_data = obs_data[np.logical_not(obs_data[:, 1] <-1)]
    obs_data = obs_data[np.logical_not(obs_data[:, 1] > 2)]
    obs_data = obs_data[np.logical_not(obs_data[:, 0] >8100)]
    localminima_data=find_localMinimas(obs_data)

    localminima_data=redshiftFinder.calcthreeSigma(localminima_data)
    localminima_data=redshiftFinder.findIndexofFluxOne(localminima_data)
    print(localminima_data)
    plt=plot_graph(obs_data, localminima_data)
    plt.axhline(y=1, color='r', linestyle='--')
    #localminima_data = localminima_data[np.logical_not(localminima_data[:, 1] > threshold_flux)]
    wavelength_range=redshiftFinder.find_wavelengthRange(redShiftrange)
    #print(wavelength_range)
    #localminima_data = localminima_data[np.logical_not(localminima_data[:, 0]  > wavelength_range[1])]
    #localminima_data = localminima_data[np.logical_not(localminima_data[:, 0]  < wavelength_range[0])]
    discovered_z= redshiftFinder.find_redshift_for_each_Ion(number_of_system, localminima_data, abs_data)
    #print(discovered_z)
    count =0
    z_average=[]
    number_of_points=[]
    #print(redShiftrange)
    for z in discovered_z:
        if(redShiftrange[0]<z<redShiftrange[1]):
           zavg,zerror,localminima, points= redshiftFinder.find_redshift_points_in_plot(z, localminima_data, abs_data)
           z_average.append((zavg, zerror))
           plot_minima_in_graph(obs_data, localminima, color[count])
           count+=1
           number_of_points.append(points)
    annotateGraph(plt, z_average, number_of_points)
    plt.title('(J10513545)Observed wavelength Vs Normalized flux')
    plt.xlabel(r'$\lambda_{obs}$')
    plt.ylabel('f 'r'$_{\lambda_{obs}}$')
    #plt.savefig('images/J10513545.png', dpi=1000)
    os.remove('/Users/sumithkuttiyilsuresh/PycharmProjects/FindRedshifts/webApp/static/img.png')
    plt.savefig('/Users/sumithkuttiyilsuresh/PycharmProjects/FindRedshifts/webApp/static/img.png')
    return obs_data

