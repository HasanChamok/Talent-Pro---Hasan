
# This code basically for reading
import cv2 as cv

#importing and showing images

# img = cv.imread('photos/1.jpg')
# cv.imshow('Cat',img)

# cv.waitKey(0)

capture = cv.VideoCapture('videos/2.mp4')

while True:
    isTrue , frame = capture.read()
    cv.imshow('Video',frame)
    
    if cv.waitKey(20) & 0xFF == ord('d'):
        break
    
    
capture.release()
cv.destroyAllWindows()
