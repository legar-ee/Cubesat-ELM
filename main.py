import os
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image

imageChannels = ["LT05_L1TP_203024_19950815_20180217_01_T1_B3.TIF",
                 "LT05_L1TP_203024_19950815_20180217_01_T1_B2.TIF",
                 "LT05_L1TP_203024_19950815_20180217_01_T1_B1.TIF"]

# Reflactance value for RGB (0-1 scale)
cloudRef = [.9,.9,.9] 
grassRef = [.12,.17,.14] # 400, 550, 600

OriginalDNs = []
CorrectedDNs = []

j = 0
#iterates through the three channels for image
for i in imageChannels:
    # Loads tiff file (1 channel)
    im = Image.open(i)

    # Converts imDNge into DN array 
    imDN = np.array(im)
    OriginalDNs.append(imDN)

    # first point is clouds, second is grassy area [1062,5088] [4603,3333] 
    p2,p1= cloudRef[j],grassRef[j]
    dn2,dn1= imDN[5088,1059], imDN[3333,4603] 

    # Modify array in some way
    gain = (p2-p1)/(dn2-dn1)
    print(gain)
    max = np.max(imDN[np.nonzero(imDN)])
    min = np.min(imDN[np.nonzero(imDN)])
    p = (imDN-min)*gain

    #append channel to list of corrected channels
    CorrectedDNs.append(p)
    j=j+1




# Display before and after images
fig, imgs = plt.subplots(1, 2)
fig.suptitle('Horizontally stacked subplots')
imgs[0].imshow(np.dstack((OriginalDNs[0],OriginalDNs[1],OriginalDNs[2])) , norm='linear', interpolation='nearest')
imgs[1].imshow(np.dstack((CorrectedDNs[0],CorrectedDNs[1],CorrectedDNs[2])), norm='linear', interpolation='nearest')
plt.show()