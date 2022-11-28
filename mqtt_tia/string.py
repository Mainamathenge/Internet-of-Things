print("Hello World")
import cv2
import numpy as np
import matplotlib.pyplot as plt


# Read image 
image = cv2.imread('pump.PNG').astype(np.uint8)

# Get contours
gray = (cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)).astype(np.uint8)
ret,thresh = cv2.threshold(gray,
                           int(image[:, :, 0].mean()),
                           int(image[:, :, 1].mean()),
                           0)
_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# Create mask
mask = np.zeros(shape=(gray.shape), dtype=np.uint8)
cv2.drawContours(mask, contours, -1, (1,0,0), cv2.FILLED)   
mask = (~(mask == 1) * 1).astype(np.uint8)

# cut off background
img_masked = cv2.bitwise_and(image, image, mask=mask)

plt.figure(figsize=(20, 20))

print("Image shape: {} | image type: {} | mask shape: {} | mask type: {}".format(X.shape, X.dtype, mask.shape, mask.dtype) )

plt.subplot(131)
plt.imshow(image)
plt.subplot(132)
plt.imshow(mask)
plt.subplot(133)
plt.imshow(img_masked)