import numpy as np
from numpy.linalg import norm
import  math
def area(a, b, c) :
    x1,y1=a
    x2,y2=b
    x3,y3=c
    area=0.5*((x2-x1)*(y3-y1)-(x3-x1)*(y2-y1))
    return area
def intersection(a, b):
    x1, y1=a
    x2, y2=b
    x=-1*y1*((x2-x1)/(y2-y1))+x1
    #x=x1+((0.5-y1)*(x2-x1)/(y2-y1))
    return [x, 0]

def calcNewArea(area,leftindex,rightindex, obs_data):

    while(leftindex<rightindex):
        #print(obs_data[leftindex][0],obs_data[leftindex+1][0], obs_data[leftindex][1])
        if(obs_data[leftindex][1]<-1):
            area=area+(obs_data[leftindex+1][0]-obs_data[leftindex][0])*-1
        else:
            area = area + (obs_data[leftindex + 1][0] - obs_data[leftindex][0]) * obs_data[leftindex][1]
        leftindex=leftindex+1
    #print('area:', area)
    return (abs(area))



def findOnecrossingPoints(obs_data):
    delta = 0
    pix = 0

    #print(obs_data[:, 4])
    obs_data[:, 1] = obs_data[:, 1] - 1
    #print(obs_data[:, 1])
    local_minima=[]
    leftcom=0
    rightcom=0
    areaprev=0
    toprint=[]
    temp = []
    leftcutnew=0
    rightcutnew=0
    for i in range(0, len(obs_data)):
        for j in range(0, 5):
            if (i - j - 1 > 0):
                delta = delta + (obs_data[i - j][0] - obs_data[i - j - 1][0])
            if (i + j + 1 < len(obs_data)):
                delta = delta + (obs_data[i + j + 1][0] - obs_data[i + j][0])
        delta = delta / 10
        pix = 0.000192308 * obs_data[i][0] + 0.769231

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
            #print(obs_data[i][0],obs_data[left][0],obs_data[right][0])
            if(left>0 and right>0):

                #print(i)
                a=[obs_data[left][0], obs_data[left][1]]
                b = [obs_data[left+1][0], obs_data[left+1][1]]
                x = [obs_data[right][0], obs_data[right][1]]
                y = [obs_data[right-1][0], obs_data[right-1][1]]
                left=left+1
                right=right-1
                leftcut=intersection(a,b)[0]
                if(obs_data[left][1]<-1):
                    leftarea=(obs_data[left][0]-leftcut)*-1
                else:
                    leftarea = (obs_data[left][0] - leftcut) * obs_data[left][1]
                rightcut=intersection(x,y)[0]
                if(delta!=0):
                  numpixel=(rightcut-leftcut)/delta
                  pix=max(pix,numpixel)

                rms=0
                sigma=0
                count=0
                for k in range(1,i):
                    if(i-k>= 0 and obs_data[i-k][0]<leftcut):
                        if(obs_data[i-k][1]+1<np.average(obs_data[:,1]+1) or obs_data[i-k][0]<leftcut-2*pix):
                            break
                        rms=rms+obs_data[i-k][1]*obs_data[i-k][1]
                        sigma=sigma+obs_data[i-k][2]
                        if(i==12):
                            print(obs_data[i-k][0],obs_data[i-k][1],obs_data[i-k][1], rms)
                        count=count+1
                for k in range(1+1,len(obs_data)-1):
                    if(k<len(obs_data) and obs_data[k][0]>rightcut):
                        if(obs_data[k][1]+1<np.average(obs_data[:,1]+1) or obs_data[k][0]>rightcut+2*pix):
                            break
                        rms=rms+obs_data[k][1]*obs_data[k][1]
                        sigma=sigma + obs_data[k][2]
                        if (i == 12):
                            print(obs_data[k][0], obs_data[k][1], obs_data[k][1], rms)
                        count=count+1
                rms=math.sqrt(rms/count)
                sigma=sigma/count
                rms=math.sqrt((rms*rms)+(sigma*sigma))
                #print('rms value is :', obs_data[i][0], rms,count,  obs_data[i][0]-pix, obs_data[i][0]+pix)
                const = 4 * delta * math.sqrt(pix) * 1000
                threesigma = const * rms
                if (obs_data[left][1] < -1):
                    rightarea = (rightcut - obs_data[right][0]) * -1
                else:
                    rightarea = (rightcut - obs_data[right][0]) * obs_data[right][1]
                #print((leftarea,rightarea))
                #print('for :', obs_data[i][0])
                area=calcNewArea((leftarea+rightarea), left, right, obs_data)*1000
                #print(obs_data[i][0], obs_data[i][1]+1, area, obs_data[i][4])
                if(leftcom!=left and rightcom !=right):
                  if(len(temp)>0):
                    temp=np.array(temp)
                    index = np.argmin(temp[:, 1])
                    sum=0
                    weight=0
                    for k in range(0, len(temp)):
                        weight=weight+temp[k][0]*(temp[k][1]+1)
                        sum=sum+temp[k][1]+1
                    weight=weight+temp[index][7]+temp[index][8]
                    sum=sum+2
                    temp[index][0]=weight/sum

                    #temp[index][0]=(temp[0][0]+temp[-1][0])/2
                    #temp[index][0]=(temp[index][7]+temp[index][8])/2
                    #print(leftcutnew, rightcutnew, temp[0][0], temp[-1][0])
                    local_minima.append((temp[index][0], temp[index][1],temp[index][2], temp[index][3], temp[index][4]))
                    #print((temp[index][0], temp[index][1], areaprev, temp[index][5]))
                    leftcom=left
                    rightcom=right
                    #print(temp)
                    temp=[]
                    center=(leftcutnew+rightcutnew)/2
                    temp.append((obs_data[i][0], obs_data[i][1], obs_data[i][2], obs_data[i][3], area - threesigma,threesigma, center, leftcut, rightcut))
                    toprint.append((obs_data[i][0], obs_data[i][1], obs_data[i][2], obs_data[i][3], area,threesigma))
                  else:
                      center = (leftcutnew + rightcutnew) / 2
                      temp.append((leftcutnew, 0, obs_data[i][1], obs_data[i][3], -1, threesigma, center, leftcut, rightcut))
                      temp.append((obs_data[i][0], obs_data[i][1], obs_data[i][2], obs_data[i][3], area - threesigma, threesigma, center, leftcut, rightcut))
                      temp.append((rightcutnew, 0, obs_data[i][1], obs_data[i][3], -1, threesigma, center, leftcut, rightcut))

                      toprint.append((obs_data[i][0], obs_data[i][1], obs_data[i][2], obs_data[i][3], area,threesigma))
                      leftcom = left
                      rightcom = right
                  #print(local_minima)
                elif(leftcom==left and rightcom ==right):
                     #print((obs_data[i][0], obs_data[i][1], area, obs_data[i][4]))
                     center = (leftcutnew + rightcutnew) / 2
                     temp.append((obs_data[i][0], obs_data[i][1], obs_data[i][2], obs_data[i][3], area - threesigma,threesigma, center, leftcut, rightcut))
                     toprint.append((obs_data[i][0], obs_data[i][1], obs_data[i][2], obs_data[i][3], area, threesigma))
                     areaprev=area
                leftcutnew=leftcut
                rightcutnew=rightcut

    #print(local_minima)
    local_minima=np.array(local_minima)
    #print(local_minima)
    local_minima[:, 1] = local_minima[:, 1] + 1
    #print(local_minima[:,4])
    #print(np.where(local_minima), local_minima[:,1]==1)


    return local_minima

