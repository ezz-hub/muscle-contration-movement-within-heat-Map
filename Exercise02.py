import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.stats
mat = scipy.io.loadmat(r'G:\_FAU matierals\Nerorscience movement\Exercise 1\Exercise 1\Slow_Contraction.mat')
mat2 = scipy.io.loadmat(r'G:\_FAU matierals\Nerorscience movement\Exercise 1\Exercise 1\Rapid_Contractions.mat')

print(len(mat["SIG"][0][0][0]))


########### print ((mat["MUPulses"][0][1][0]))
##### print (len(mat["MUPulses"][0][0][0]))


allSamplesArray=[]
for m in range(0,len(mat["MUPulses"][0])):
    for s in range(0,len(mat["MUPulses"][0][m][0])):
        allSamplesArray.append(mat["MUPulses"][0][m][0][s])


print(len(allSamplesArray))
allSamplesArray=list(dict.fromkeys(allSamplesArray))
print(len(allSamplesArray))

allSamplesArray.sort()

arrayInd=[]
ArrayVal=[]


    
for m in range(0,len(mat["MUPulses"][0])):
    ArrayVal.clear()
    for s in range(0,len(mat["MUPulses"][0][m][0])):
        for x in allSamplesArray:
            if mat["MUPulses"][0][m][0][s]==x:
                ArrayVal.append(x)
            else:
                ArrayVal.append(0)
    arrayInd.append(ArrayVal)



############ print(arrayInd[0])


############## mssc=[1,2,3,5,4,6,11]


################### plt.matshow(np.array(arrayInd))

sscd=[]
for m in range(0,len(mat["MUPulses"][0])):
    sscd.append(m)


xs=[1,2,3,4]
ys=[[5,7,8],[2,3],[1,2],[7,4]]
for l in range(0,len(arrayInd)):
    print(l)
    for m in range(0,len(mat["MUPulses"][0][l][0])):    
        plt.scatter(sscd[l], mat["MUPulses"][0][l][0][m])

plt.show()

EMG=mat2["SIG"][0][0][0]
ref_signal=mat2["ref_signal"][0]


T=[]
for i in range (0,len(ref_signal)):
    T.append((1/2048)*i)

plt.plot(T, ref_signal, color='g',label='Signal')

####The way this will be done is that we will look for peaks in each of the 64 signals but
#### make error of 5% for example which will remove the point of one channel is the peak was already so close to 
####another channel then will make the same with lowest part and check the distance and average to make 
####estimation of best window size

Max=0
MaxT=0
MaxVec=[]


Min=99999
MinT=0
MinVec=[]
RealMaxVec=[]
#### print(len(mat2["SIG"][0][0][0]))

for m in range(0,len(mat2["SIG"])):
    Max=0
    Min=99999
    for s in range (0,len(mat2["SIG"][m])):
        for t in range(0,len(mat2["SIG"][m][s])):
            for K in range(0,len(mat2["SIG"][m][s][t])):
                if(mat2["SIG"][m][s][t][K]>Max):
                    Max=mat2["SIG"][m][s][t][K]
                    MaxT=T[K]
                if(mat2["SIG"][m][s][t][K]<Min):
                    Min=mat2["SIG"][m][s][t][K]
                    MinT=T[K]
        MaxVec.append(MaxT)
        MinVec.append(MinT)












print("!!!!!!!!!!!!")
print(len(MaxVec))

### print(MinVec)
### print(MinVec)

MaxVecNew=[]
MinVecNew=[]


###The Max point were 19 and min was 4 at error level of 5 so had to increase in case of peaks
for inc in range(0,len(MaxVec)):
    for m in range(0,len(MaxVec)):

        ###print(abs(MaxVec[inc]-MaxVec[m]))
        ### print(0.5* MaxVec[len(MaxVec) -1 ])
        ### print(0.5* T[len(T) -1 ])
        ###The 0.1 and 0.2 are estimated cause the signal should not be too close or too far so something that will 
        ###divide the signal into 5 partions for example so less than 0.2 and not too small and not zero to cover
        ###boundries so 0.1 
        if(abs(MaxVec[inc]-MaxVec[m])> 0.3* T[len(T) -1 ]  and  abs(MaxVec[inc]-MaxVec[m]) <0.4* T[len(T) -1 ] ):
            MaxVecNew.append(MaxVec[inc])
        if(abs(MinVec[inc]-MinVec[m])> 0.3* T[len(T) -1 ]  and  abs(MinVec[inc]-MinVec[m]) <0.4* T[len(T) -1 ] ):
            MinVecNew.append(MinVec[inc])
        
  
        
            
MaxVecNew=list(dict.fromkeys(MaxVecNew))
    
MinVecNew=list(dict.fromkeys( MinVecNew))

##### print(MinVecNew)

##### print(MaxVecNew)

FloorMin=[]
FloorMax=[]

for i in MaxVecNew:
    FloorMax.append(math.floor(i))
    pass

for iss in MinVecNew:
    FloorMin.append(math.floor(iss))



FloorMax=list(dict.fromkeys(FloorMax))
    
FloorMin=list(dict.fromkeys( FloorMin))
##### print(FloorMax)
#### print(FloorMin)

MsArray=[]
for s in range (0,len(FloorMax)):
    Minss=99999
    for ms in range (0,len(FloorMin)):
        if(abs(FloorMax[s]-FloorMin[ms]) <Minss):
            Minss=abs(FloorMax[s]-FloorMin[ms])
    MsArray.append(Minss)


#### print(MsArray)

mmps=np.array(MsArray)
#### print(np.average(mmps))


### so the window size will ve this average *2
window_Size=np.average(mmps)*2

for m in range(0,len(T)):
    if T[m]>window_Size:
        window_Size=m
        break



TheIndexess=[]
TheIndexessArray=[]

TheMaxVecArrayM=[]
for m in range(0,len(mat["MUPulses"][0])):
    RealMaxVec.clear()
    for s in range(0,len(mat["MUPulses"][0][m][0])):
        RealMaxVec.append(mat["MUPulses"][0][m][0][s])
    TheMaxVecArrayM.append(RealMaxVec)
    

# print(TheMaxVecArrayM)

TheSupremeeIndex=[]


# will change here len(TheMaxVecArrayM) to just 2 cause of speed
for msscs in range(28,30):
    TheIndexessArray.clear()
    print(msscs)
    for MaxVecm in range (0,len(TheMaxVecArrayM[msscs])):
        TheIndexess.clear()
        for Kindex in range(0,len(T)):
            # print(Kindex)
            if Kindex>=int(int(TheMaxVecArrayM[msscs][MaxVecm])-window_Size) and  Kindex<=int(int(TheMaxVecArrayM[msscs][MaxVecm])+window_Size) :      
                TheIndexess.append(Kindex)
        TheIndexessArray.append(TheIndexess)
    TheSupremeeIndex.append(TheIndexessArray)

print("YYYYYYYYYYYYYY")
# print(TheSupremeeIndex)


# TheMaxOfChannels=[]
# for K in range(TheIndexess[0],TheIndexess[len(TheIndexess)-1]+1):
#     Sum=0
#     for m in range(0,len(mat2["SIG"])):
#         for s in range (0,len(mat2["SIG"][m])):
#             for t in range(0,len(mat2["SIG"][m][s])):
#                 Sum=Sum+mat2["SIG"][m][s][t][K]
#     TheMaxOfChannels.append(Sum/64)


FirstOne=True
TheSuperSum=[]
KcounterArray=[]
TheSupremeeeSum=[]
for mK in range(0,len(TheSupremeeIndex)):
    TheSuperSum.clear()
    for m in range(0,len(mat2["SIG"])):
        print(m)
        print(FirstOne)
        for s in range (0,len(mat2["SIG"][m])):
            KCounter=0
            Sum=[]
            FirstOne=True    
            for t in range(0,len(mat2["SIG"][m][s])):
                    for stL in range(0,len(TheSupremeeIndex[mK])):
                        KCounter+=1
                        for K in range(TheSupremeeIndex[mK][stL][0] ,(TheSupremeeIndex[mK][stL][len(TheSupremeeIndex[mK][stL])-1])+1):
                            if FirstOne==True:
                                Sum.append(mat2["SIG"][m][s][t][K])
                            else:
                                # print(K)
                                # print(TheIndexessArray[stL][0])
                                Sum[K-TheSupremeeIndex[mK][stL][0]]=Sum[K-TheSupremeeIndex[mK][stL][0]]+mat2["SIG"][m][s][t][K]
                        FirstOne=False
            TheSuperSum.append(Sum)
            KcounterArray.append(KCounter)
    TheSupremeeeSum.append(TheSuperSum)
    

                    
                    
                





# print(TheSuperSum[0][500:550])
# print(TheSuperSum[1][500:550])

# print("!!!!!!!!!!!!!!!!!!!!!!!!!!@!E##$")


print(len(TheIndexessArray))
print("OHHHHHHHHHHHHH")
print(len(TheSupremeeeSum))
# print(TheSupremeeIndex)

print(len(TheSupremeeeSum[0][0]))



# plt.xlabel('Time')
# plt.ylabel('Signal')
# plt.show()


SampleArray=[]
TheAVGArrays=[]
for s in range (0,len(TheSupremeeeSum[0][0])):
    SampleArray.append(s)


for m in range(0,len(TheSupremeeeSum[0])):
    THEAVG=np.array(TheSupremeeeSum[0][m])
    THEAVG=np.divide(THEAVG,65)
    TheAVGArrays.append(THEAVG)

TheRMS=[]
THEMajorRMS=[]
for t in TheSupremeeeSum:
    TheRMS.clear()
    for s in t:
        SumSquare=0
        for k in s:
            SumSquare=SumSquare+k**2
        TheRMS.append(math.sqrt(SumSquare))
    THEMajorRMS.append(TheRMS)
    

print("!!!!!!!!!!!!!!!!!!!!!!!!!")    
print(len(TheRMS))


plt.plot(SampleArray, TheAVGArrays[12], color='g',label='Signal')

plt.xlabel('Time')
plt.ylabel('Average')
plt.show()



def heatmap2d(arr: np.ndarray):
    plt.imshow(arr, cmap='viridis')
    plt.colorbar()
    plt.show()






test_array = np.array(THEMajorRMS[1]).reshape(13, 5)
heatmap2d(test_array)





