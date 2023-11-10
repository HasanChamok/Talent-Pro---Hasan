import cv2 as cv

import numpy as np


img = cv.imread('photos/1.jpg')
cv.imshow('Real Image',img)


#contours is like number of edges in a file 

blank = np.zeros(img.shape,dtype=np.uint8)
# cv.imshow('Blank',blank)

gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.imshow('Gray',gray)


#bluring an image will reduce the amount of contours
# canny = cv.Canny(img,125,175)
# cv.imshow('Canny Edges',canny)

ret, trash = cv.threshold(gray,125,255,cv.THRESH_BINARY)
# cv.imshow("Threshoulded image", trash)

contours, hierarchies = cv.findContours(trash, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
print(f'{len(contours)} countor(S) found')


cv.drawContours(blank,contours,-1,(0,0,255),1)
cv.imshow('Contours Drawn',blank)

cv.waitKey(0)