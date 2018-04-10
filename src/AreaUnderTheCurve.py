import numpy as np
from numpy.linalg import norm

def area(a, b, c) :
    x1,y1=a
    x2,y2=b
    x3,y3=c
    area=0.5*((x2-x1)*(y3-y1)-(x3-x1)*(y2-y1))
    return area
def intersection(a, b):
    x1, y1=a
    x2, y2=b
    x=y1*((x2-x1)/(y2-y1))+x1
    x=x1+((0.5-y1)*(x2-x1)/(y2-y1))
    return [x, 0]




def findOnecrossingPoints(obs_data):
    temp_list=[]
    temp_list.append((1-obs_data[:,1])/obs_data[:,2]*1000-obs_data[:,3])
    obs_data=np.concatenate((obs_data,np.transpose(temp_list)),axis=1)

    return obs_data
