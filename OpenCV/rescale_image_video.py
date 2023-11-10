
import cv2 as cv

def rescaleFrame(frame,scale=0.75):
    #this will work for image , video , live video
    width = int(frame.shape[1]*scale)
    height = int(frame.shape[0]*scale)
    
    dimensions = (width,height)
    
    return cv.resize(frame,dimensions,interpolation=cv.INTER_AREA)

def changeRes(width,height):
    #this will only work for Live videos
    capture.set(3,width)
    capture.set(4,height)

img = cv.imread('photos/1.jpg')
cv.imshow('Cat',img)

# cv.waitKey(0)

capture = cv.VideoCapture('videos/2.mp4')



resized_image = rescaleFrame(img,scale=0.5)
cv.imshow('Image',resized_image)

while True:
    isTrue , frame = capture.read()
    frame_resized = rescaleFrame(frame,scale=0.2)
    cv.imshow('Video',frame)
    cv.imshow('Video Resized',frame_resized)
    
    if cv.waitKey(20) & 0xFF == ord('d'):
        break
    
    
capture.release()
cv.destroyAllWindows()