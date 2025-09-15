import os
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image


def compare(imCalc,imTruth):
    imDiff = np.abs((imTruth-imCalc)/((imTruth+imCalc)/2) + 1e-7) # My IDE says there are some division issues so I add a small offset
    return(imDiff)



testImageChannels = ["./TestImage/LT05_L1TP_203024_19950815_20180217_01_T1_B3.TIF",
                 "./TestImage/LT05_L1TP_203024_19950815_20180217_01_T1_B2.TIF",
                 "./TestImage/LT05_L1TP_203024_19950815_20180217_01_T1_B1.TIF"]
groundTruthChannels = ["./groundTruthImage/LT05_L2SP_203024_19950815_20200912_02_T1_SR_B3.TIF",
                       "./groundTruthImage/LT05_L2SP_203024_19950815_20200912_02_T1_SR_B2.TIF",
                       "./groundTruthImage/LT05_L2SP_203024_19950815_20200912_02_T1_SR_B1.TIF"]

# Reflactance value for RGB (0-1 scale)
cloudRef = [.9,.9,.9] 
grassRef = [.12,.17,.14] # 400, 550, 600

OriginalDNs = []
CorrectedDNs = []
GroundTruthScalingFactors = []
GroundTruthDNs = []
ComparisonPercents = []

j = 0
#iterates through the three channels for image
for i in testImageChannels:
    # Loads tiff file (1 channel)
    im = Image.open(i)

    # Converts image into DN array 
    imDN = np.array(im)

    # calculate gain
    # first point is clouds, second is grassy area [1062,5088] [4603,3333] 
    p2,p1= cloudRef[j],grassRef[j]
    dn2,dn1= imDN[5088,1059], imDN[3333,4603] 
    gain = (p2-p1)/(dn2-dn1)
    offset = p2 - gain*dn2 # Added the offest
    print(gain)

    p = gain*imDN + offset # I removed the normalized DN 

    
    #append channel to list of corrected channels
    CorrectedDNs.append(p)
    OriginalDNs.append(imDN)
    
    # Find min and max for use with scaling groundtruth to same values
    min = np.min(p)
    max = np.max(p)
    coeffTuple = (min,max)
    print(coeffTuple)
    GroundTruthScalingFactors.append(coeffTuple)
    j=j+1


# setup Ground Truth image for calcs + Viewing (0 - 1)
k = 0
for i in groundTruthChannels:
    scale = GroundTruthScalingFactors[k]
    im2 = Image.open(i)
    imTruth = np.array(im2)
    imTruth = (((imTruth - np.min(imTruth))/(np.max(imTruth)-np.min(imTruth)) * (scale[1]-scale[0]) + scale[0]))
    GroundTruthDNs.append(imTruth)
    k=k+1



# compare percent difference by averaging percent difference at each pixel for all 3 channels
comparisonImg = compare(CorrectedDNs[0],GroundTruthDNs[0])

# Display before and after images
fig, imgs = plt.subplots(1, 3)
fig.suptitle('Before, After, GroundTruth')

#Original (Uncorrected)
imgs[0].imshow(np.dstack((OriginalDNs[0],OriginalDNs[1],OriginalDNs[2])), interpolation='nearest')
# Corrected
imgs[1].imshow(np.dstack((CorrectedDNs[0],CorrectedDNs[1],CorrectedDNs[2])), interpolation='nearest')
# Ground Truth
imgs[2].imshow(np.dstack((GroundTruthDNs[0],GroundTruthDNs[1],GroundTruthDNs[2])), interpolation='nearest')





# Shows percent difference between corrected and ground truth
fig, ax = plt.subplots()
im = ax.imshow(comparisonImg,cmap="viridis")
ax.axis("off")
fig.suptitle('Calculated vs Groundtruth Percent Difference (0 - 1.0) for Red Channel')
fig.colorbar(im)
plt.show()


