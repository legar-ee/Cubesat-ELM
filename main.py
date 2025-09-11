import os
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image

imageChannels = ["LT05_L1TP_203024_19950815_20180217_01_T1_B3.TIF","LT05_L1TP_203024_19950815_20180217_01_T1_B2.TIF","LT05_L1TP_203024_19950815_20180217_01_T1_B1.TIF"]
OriginalDNs = []
CorrectedDNs = []


#iterates through the three channels for image
for i in imageChannels:
    # Loads tiff file (1 channel)
    im = Image.open(i)

    # Converts imDNge into DN array
    imDN = np.array(im)
    print(imDN.shape) # Sanity check for array shape

    OriginalDNs.append(imDN)


    # Modify array in some way
    gain = 1 #assumption for now
    offset=np.min(imDN[np.nonzero(imDN)]) - 1 # current offset is lowest non-zero pixel - 1
    imDN = gain * imDN + offset 

    #Convert array back to imDNge
    imMod = Image.fromarray(imDN)

    #append channel to list of corrected channels
    CorrectedDNs.append(imDN)




# Display before and after images
fig, imgs = plt.subplots(1, 2)
fig.suptitle('Horizontally stacked subplots')
imgs[0].imshow(np.dstack((OriginalDNs[0],OriginalDNs[1],OriginalDNs[2])))
imgs[1].imshow(np.dstack((CorrectedDNs[0],CorrectedDNs[1],CorrectedDNs[2])))
plt.show()