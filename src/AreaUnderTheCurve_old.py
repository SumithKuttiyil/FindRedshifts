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

def calcNewArea(area,leftindex,rightindex, obs_data):
    while(leftindex<rightindex):
        area=area+(obs_data[leftindex+1][0]-obs_data[leftindex][0])*obs_data[leftindex][1]
        leftindex=leftindex+1
    return (abs(area))



def findOnecrossingPoints(obs_data):
    #print(obs_data[:, 1])
    obs_data[:, 1] = obs_data[:, 1] - 1
    #print(obs_data[:, 1])
    local_minima=[]
    leftcom=0
    rightcom=0
    temp = []
    for i in range(0, len(obs_data)):
        if(obs_data[i][1]<0):

            #print('hai')
            left=0
            right=0
            for j in range(1, i):
                #print(i-j,obs_data[i-j][1] )
                if(i-j>=0 and obs_data[i-j][1]>0):
                    left=i-j

                    break
            for j in range(i+1, len(obs_data)-1):
                if(j<len(obs_data) and obs_data[j][1]>0):
                    right=j
                    #print(j,obs_data[j][1] )
                    break
            if(left>0 and right>0):
                #print(i)
                a=[obs_data[left][0], obs_data[left][1]]
                b = [obs_data[left+1][0], obs_data[left+1][1]]
                x = [obs_data[right][0], obs_data[right][1]]
                y = [obs_data[right-1][0], obs_data[right-1][1]]
                left=left+1
                right=right-1
                leftcut=intersection(a,b)[0]
                leftarea=(obs_data[left][0]-leftcut)*obs_data[left][1]
                rightcut=intersection(x,y)[0]
                rightarea = (rightcut-obs_data[right][0]) * obs_data[right][1]
                area=calcNewArea((leftarea+rightarea), left, right, obs_data)*1000
                #print(obs_data[i][0], obs_data[i][1]+1, area, obs_data[i][4])
                if(leftcom!=left and rightcom !=right):
                  if(len(temp)>0):
                    temp=np.array(temp)
                    index = np.argmin(temp[:, 1])
                    local_minima.append((temp[index][0], temp[index][1],temp[index][2], temp[index][3], area-temp[index][4]))
                  leftcom=left
                  rightcom=right
                  #print(temp)
                  temp=[]
                  #print(local_minima)
                elif(leftcom==left and rightcom ==right):
                    temp.append((obs_data[i-1][0], obs_data[i-1][1], obs_data[i-1][2], obs_data[i-1][3], area - obs_data[i-1][4]))
                    print((obs_data[i][0], obs_data[i][1], area, obs_data[i][4]))
                    temp.append((obs_data[i][0], obs_data[i][1], obs_data[i][2], obs_data[i][3], area - obs_data[i][4]))


    #print(local_minima)
    local_minima=np.array(local_minima)
    #print(local_minima)
    local_minima[:, 1] = local_minima[:, 1] + 1
    #print(local_minima[:,4])
    #print(np.where(local_minima), local_minima[:,1]==1)
    return local_minima

