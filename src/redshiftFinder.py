import  numpy as np
import  pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import  argrelextrema
from  collections import Counter
import  math as math
from src import  AreaUnderTheCurve_old

threshold_flux = 0.9
#ions_interest=['Mg II','Fe II']
#ions_interest=['Mg II','Fe II','C IV']
#ions_interest=['Si IV', 'C IV', 'C II', 'O I', 'Fe II']
#ions_interest=['O I','C II']
delta_lambda=0.304
hash_pix=2.9
discovered_z = []
decimal=4


#Find the highest occuring redshift for each ion and return red shuft curresposing to each ion
def find_redshift_for_each_Ion(number_of_system, localminima_data, abs_data, ions):
    global ions_interest
    ions_interest=ions
    #print('ions:----', ions, ions_interest)
    #print('number of lines:-', localminima_data.size)
    counter=0
    #threshold_flux=np.average(localminima_data[:, 1])
    z_temp = []

    if(number_of_system==1):
      delete=[]
      for i in abs_data[:,1]:
        for j in localminima_data[:,0]:
            if (str(abs_data[counter][0]+' '+str(abs_data[counter][1]))  in ions_interest):
               z_temp.append((j/i)-1)
               delete.append((i, j, (j/i)-1))
        counter += 1
      z_predicted=Counter(np.round(z_temp, decimal)).most_common(5)[0][0]
      #print(z_temp)
      #print('system %i' % number_of_system)
      print(Counter(np.round(z_temp, decimal)).most_common(10))
      discovered_z.append(z_predicted)
      li=[]
      li.append(z_predicted)
      return li

    else:
        #print('abs_data is printed', abs_data)
        #print('localminima_data is printed', localminima_data)
        if(np.size(abs_data)==0):
            return 0
        for i in abs_data[:, 1]:
            #print(localminima_data[:, 0])
            for j in localminima_data[:, 0]:
                #print('ione is there', ions_interest)
                if(str(abs_data[counter][0])+' '+str(abs_data[counter][1]) in ions_interest):
                   z_temp.append((j / i) - 1)
                   #print('hi inside', z_temp)
            counter += 1
        #print('z_temp is printed:----', z_temp)
        z_predicted=Counter(np.round(z_temp, decimal)).most_common(2)[0][0]
        #print('system %i'%number_of_system)
        print(Counter(np.round(z_temp, decimal)).most_common(10))
        discovered_z.append(z_predicted)
        localminima_data=remove_discovered_line(z_predicted, localminima_data, abs_data)
        number_of_system-=1
        find_redshift_for_each_Ion(number_of_system,localminima_data,abs_data, ions)
        return discovered_z


def remove_discovered_line(redshift, localminima_data, abs_data):
    temp_minima=[]
    count = 0
    for j in localminima_data[:, 0]:
        for i in abs_data:
            if (str(i[0])+' '+str(i[1]) in ions_interest):
               z=((j / i[1]) - 1)
               if((redshift-0.01)<z and (redshift+0.01)>z):
                  break

            if(abs_data[-1][1]==i[1]):
               temp_minima.append((localminima_data[count][0], localminima_data[count][1]))

        count +=1
    return np.array(temp_minima)


def find_zaverage(redshift, localminima_data, abs_data):
    redshiftPoints = []
    find_z_average = []
    for i in abs_data[:, 1]:
        count = 0
        for j in localminima_data[:, 0]:
            if ((redshift - 0.01) < ((j / i) - 1) and (redshift + 0.01 > ((j / i) - 1))):
                find_z_average.append((j / i) - 1)
            count += 1

    #print('average of redshit:-', np.average(find_z_average), math.sqrt(np.var(find_z_average)))
    zavg, zerror = np.average(find_z_average), math.sqrt(np.var(find_z_average))
    return (zavg,zerror)

def find_redshift_points_in_plot(redshift, localminima_data, abs_data):
    redshiftPoints=[]
    zavg,zerror=find_zaverage(redshift, localminima_data, abs_data)
    num_of_points = 0
    common_wav_loc= 0
    for i in abs_data:
        count = 0

        for j in localminima_data[:, 0]:
                if ((zavg - zerror) < ((j / i[1]) - 1) and (zavg+zerror> ((j / i[1]) - 1))):

                    redshiftPoints.append((j, localminima_data[count][1], i[1],i[0]))
                    if(common_wav_loc!=i[1]):
                        num_of_points += 1
                    common_wav_loc=i[1]
                count+=1


    return (zavg,zerror,np.array(redshiftPoints), num_of_points)


def find_wavelengthRange(range):
    HI=1025.7223
    NaI=2600.5581
    lamL=(range[0]+1)*HI
    lamH=(range[1]+1)*NaI
    #print(lamL, lamH)
    return [lamL, lamH]

def addError(obs_data):
    obs_data[:,1]=obs_data[:,1]+obs_data[:,2]
    return obs_data

def calcthreeSigma(obs_data):
    temp_list=[]
    const=3*delta_lambda*math.sqrt(hash_pix)*1000
    #print(delta_lambda, hash_pix, const)
    temp_list.append(const*obs_data[:,2])
    #for val in obs_data[:,2]:
        #print(val)
        #temp_list.append(const*val)
    #temp_list=np.array(temp_list)




    #temp_list.reshape(len(temp_list),1)
    print(np.shape(temp_list), np.shape(obs_data))
    obs_data = np.concatenate((obs_data, np.transpose(temp_list)), axis=1)
    print(obs_data[:,4])
    return obs_data

def areaUnderTheCurve(obs_data):

    temp_list=[]
    #print('111111', ((1 - obs_data[0, 1]) / obs_data[0, 2] )* 1000)
    temp_list.append(((1-obs_data[:,1])/obs_data[:,2])*1000-obs_data[:,3])
    obs_data=np.concatenate((obs_data,np.transpose(temp_list)),axis=1)


    return obs_data

def findIndexofFluxOne(obs_data):
    localMinima=AreaUnderTheCurve_old.findOnecrossingPoints(obs_data)
    localMinima = localMinima[np.logical_not(localMinima[:, 4] < 0)]
    print(localMinima)
    return localMinima











