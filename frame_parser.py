import cv2 as cv

capture = cv.VideoCapture('TelloVideo/afternoon.mp4')
frames_to_skip = None # number of frames to skip between saves
frame_num = 0
file_name_num = 0
while(True):
    success, frame = capture.read()
    if success:
        if frame_num%frames_to_skip == 0:
            cv.imwrite('afternoon_{}.jpg'.format(file_name_num), frame) # save the image 
            file_name_num+=1
    else:
        break
    frame_num+=1
capture.release()