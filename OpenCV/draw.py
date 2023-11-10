import cv2 as cv
import numpy as np

blank = np.zeros((500,500,3), dtype=np.uint8)

# cv.imshow('Blank', blank)

#pint the image with certain color
# blank[200:300,300:400] = 0,255,0

# cv.imshow('Green',blank)


#Draw a rectangle
# cv.rectangle(blank, (0,0), (255,255), (0,255,0), thickness=2)
# cv.imshow('rectangle', blank)

# cv.rectangle(blank, (0,0), (255,500), (0,255,0), thickness=cv.FILLED)
# cv.imshow('rectangle', blank)

# cv.rectangle(blank, (0,0), (blank.shape[1]//2, blank.shape[0]//2), (0,255,0), thickness=cv.FILLED)
# cv.imshow('rectangle', blank)


# #Draw a circle
# cv.circle(blank,(blank.shape[1]//2,blank.shape[0]//2),40,(0,0,255),thickness=cv.FILLED)
# cv.imshow('Circle',blank)

# #Draw a Line
# cv.line(blank,(0,0),(blank.shape[1]//2,blank.shape[0]//2),(255,255,0),thickness=5)
# cv.imshow("Line",blank)

#Draw a text
cv.putText(blank,'Hello,My name is Hasan',(blank.shape[1]//2,blank.shape[0]//2),cv.FONT_HERSHEY_TRIPLEX,1.0,(2,45,222),thickness=3)
cv.imshow("TEXT",blank)


cv.waitKey(0)