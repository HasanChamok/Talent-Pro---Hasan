import cv2 as cv

img = cv.imread('photos/3.webp')
# cv.imshow("Original",img)

#convrting to grayscale
# gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
# cv.imshow("GRAY",gray)

#Blur an image
# blur = cv.GaussianBlur(img,(5,5),cv.BORDER_DEFAULT)
# cv.imshow('Blur',blur)

# #Detecting Cunny Edges
cunny = cv.Canny(img,125,125)
cv.imshow('Cunny Edges',cunny)

# #Dialted Images
# dialated = cv.dilate(cunny,(7,7),iterations=3)
# cv.imshow('Dialated',dialated)

# #Erotaded Images
# erotate = cv.erode(dialated,(7,7),iterations=3)
# cv.imshow('Erodad',erotate)


#resize image
resized = cv.resize(img,(500,500),interpolation=cv.INTER_LINEAR)
cv.imshow('Resized',resized)

#cropping image
crop = img[50:100,100:200]
cv.imshow('Cropped',crop)


cv.waitKey(0)