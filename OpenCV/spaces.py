import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


img = cv.imread('photos/2.jpg')
cv.imshow('Image',img)

#BGR to HSV
hsv  = cv.cvtColor(img,cv.COLOR_BGR2HSV)
cv.imshow('HSV Image',hsv)

#BGR to l*a*b
lab  = cv.cvtColor(img,cv.COLOR_BGR2LAB)
cv.imshow('HSV Image',lab)

#BGR to RGB
rgb  = cv.cvtColor(img,cv.COLOR_BGR2RGB)
cv.imshow('RGB Image',rgb)

cv.waitKey(0)

plt.imshow(img)
plt.show()