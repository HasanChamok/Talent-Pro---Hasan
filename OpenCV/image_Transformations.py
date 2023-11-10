import cv2 as cv
import numpy as np

img = cv.imread('photos/2.jpg')

cv.imshow('3 No Image',img)


#Translateing the image
def translate(img, x, y):
    transMate = np.float32([[1,0,x],[0,1,y]])
    dimensions = (img.shape[1],img.shape[0])
    
    return cv.warpAffine(img,transMate,dimensions)

#-x ---> Left
#-Y ---> up
#X ---> Right
#Y --> Down


translated = translate(img,100,100)
cv.imshow('Translated',translated)


#Rotating image
def rotate(img, angle, rotPoint = None):
    (height, width) = img.shape[:2]
    
    if rotPoint is None:
        rotPoint = (width//2,height//2)
        
    rotMat = cv.getRotationMatrix2D(rotPoint,angle,1.0)
    dimensions = (width,height)
    
    return cv.warpAffine(img, rotMat, dimensions)

#positive value --> anti-clockwise
#negative value --> clockwise

rotated = rotate(img,45)
cv.imshow('Rotated',rotated)


#Resized image
resized = cv.resize(img,(500,500),interpolation=cv.INTER_CUBIC)
cv.imshow('Resized', resized)

#fliping image
flip = cv.flip(img,0)
cv.imshow('Vertical Flip',flip)

#fliping image
flip = cv.flip(img,1)
#-1 will do the vertical and horizontal both
cv.imshow('Horizontal Flip',flip)

cv.waitKey(0)