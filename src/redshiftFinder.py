import  numpy as np
import  pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import  argrelextrema
from  collections import Counter
import  math as math
from src import  AreaUnderTheCurve_old

threshold_flux = 0.9
#calculate del lambda for each observed wavelength
delta_lambda=0.304

#xshooter, hash_pix=2.9
#nspec264, hash_pix=1.74,

#one point=(3800, 1500) y=0.000192308x+0.769231
#second point=(9000, 2500)

hash_pix=1.74
discovered_z = []
decimal=2


#Find the highest occuring redshift for each ion and return red shuft curresposing to each ion
def find_redshift_for_each_Ion(number_of_system, localminima_data, abs_data, ions):

    global ions_interest
    ions_interest=ions
    counter=0
    z_temp = []
    z_round=[]

    if(number_of_system==1):

      for i in abs_data[:,1]:
        i=float(i)
        for j in localminima_data[:,0]:
               z_temp.append((j/i)-1)
        counter += 1
      z_predicted=Counter(np.round(z_temp, decimal)).most_common(5)[0][0]
      print(Counter(np.round(z_temp, decimal)).most_common(10))
      discovered_z.append(z_predicted)

      return 0

    else:
        if(np.size(abs_data)==0):
            return 0
        for i in abs_data[:, 1]:
            i = float(i)
            #print('888888888888888888888888888888888888888888888888888888', i)
            for j in localminima_data[:, 0]:
                   z_temp.append((j / i) - 1)
                   z_round.append(round(j/i-1, decimal))
                   #print(j/i-1, round(j/i-1, decimal),j, i )
            counter += 1
        #print(z_temp)
        z_predicted=Counter(np.round(z_temp, decimal)).most_common(2)[0][0]
        print(Counter(np.round(z_temp, decimal)).most_common(10))
        #print(Counter(z_round).most_common(10))
        discovered_z.append(z_predicted)
        localminima_data=remove_discovered_line(z_predicted, localminima_data, abs_data)
        number_of_system-=1
        find_redshift_for_each_Ion(number_of_system,localminima_data,abs_data, ions)
        return discovered_z


def remove_discovered_line(redshift, localminima_data, abs_data):
    temp=[]
    var=len(localminima_data)-1

    for j in range(0,var):
        count = 0
        for i in abs_data:
            count=count+1
            #print(j)
            z=((localminima_data[j][0] / float(i[1])) - 1)
            if((redshift-0.01)<z and (redshift+0.01)>z):
                break
            else:
                if(count==len(abs_data)):
                  temp.append((localminima_data[j][0], localminima_data[j][1],localminima_data[j][2], localminima_data[j][3],localminima_data[j][4]))
                  break;
    return np.array(temp)


def find_zaverage(redshift, localminima_data, abs_data):
    find_z_average = []
    for i in abs_data[:, 1]:
        i = float(i)
        count = 0
        for j in localminima_data[:, 0]:
            if ((redshift - 0.01) < ((j / i) - 1) and (redshift + 0.01 > ((j / i) - 1))):
                find_z_average.append((j / i) - 1)
            count += 1

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

                if ((zavg - zerror) < ((j / float(i[1])) - 1) and (zavg+zerror> ((j / float(i[1])) - 1))):

                    redshiftPoints.append((j, localminima_data[count][1], float(i[1]),i[0], i[2]))
                    if(common_wav_loc!=float(i[1])):
                        num_of_points += 1
                    common_wav_loc=float(i[1])
                count+=1
    ionFound=set(np.array(redshiftPoints)[:,3])
    for ion in ionFound:
        #for sub list
        e=[element for element in redshiftPoints if ion == element[3]]
        e=np.array(e)
        sortedList=e[e[:,4].argsort()]
        print('**************************')
        print(sortedList)
        #for main list
        eMain=[element for element in abs_data if ion == element[0]]
        eMain = np.array(eMain)
        sortedMainList = eMain[eMain[:, 2].argsort()]
        print(sortedMainList)
        print('**************************')
    return (zavg,zerror,np.array(redshiftPoints), num_of_points)




def addError(obs_data):
    obs_data[:,1]=obs_data[:,1]+obs_data[:,2]
    return obs_data

def calcthreeSigma(obs_data):
    temp_list=[]
    delta=0
    pix=0
    for i in range(0, len(obs_data)):
        for j in range(0,5):
            if(i-j-1>0):
                delta=delta+(obs_data[i-j][0]-obs_data[i-j-1][0])
            if(i+j+1<len(obs_data)):
                delta = delta + (obs_data[i + j+1][0] - obs_data[i+ j][0])

        delta=delta/10
        pix=0.000192308*obs_data[i][0]+0.769231
        #print(pix)

        const=3*delta*math.sqrt(pix)*1000
        #print(const*obs_data[i][2])
        temp_list.append(const*obs_data[i][2])
        #print(obs_data[i][0], delta, pix, obs_data[i][2], const*obs_data[i][2])
    temp_list=np.reshape(temp_list, (len(temp_list), 1))
    #print(np.shape(temp_list), np.shape(obs_data))

    obs_data = np.concatenate((obs_data, temp_list), axis=1)
    #print(obs_data[:,4])
    return obs_data

def areaUnderTheCurve(obs_data):

    temp_list=[]
    temp_list.append(((1-obs_data[:,1])/obs_data[:,2])*1000-obs_data[:,3])
    obs_data=np.concatenate((obs_data,np.transpose(temp_list)),axis=1)


    return obs_data

def findIndexofFluxOne(obs_data):
    localMinima=AreaUnderTheCurve_old.findOnecrossingPoints(obs_data)

    localMinima = localMinima[np.logical_not(localMinima[:, 4] < 0)]

    #print(localMinima)
    return localMinima











