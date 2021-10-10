# Import Libraries
import numpy as np
import cv2
import time

# video is captured in the first 3 seconds after running the program.
cap = cv2.VideoCapture(0)
time.sleep(3)
background = 0
#To Capture the Image of the background
for i in range(60):
    ret, background = cap.read()
#the code will run only if the webcam is opened.
while(cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # Here we take the values of the selected color cloth(Red) and change  till then the selected color
    # (Red)  start to disappear from the frame.
    low_color = np.array([0,120,70])
    up_color = np.array([10,255,255]) # values is for red colour Cloth
    mask_1 = cv2.inRange(hsv, low_color, up_color)
    low_color  = np.array([170,120,70])
    up_color= np.array([180,255,255])
    mask_2 = cv2.inRange(hsv,low_color, up_color)
    #Combining the masks so that it can be viewd as in one frame
    mask_1 = mask_1 + mask_2
    #After combining the mask we are storing the value in deafult mask.

    # Using Morphological Transformations to remove the noise from the cloth and unnecessary Details
    # here, it removes the white region on the boundary of the cloth that is not required
    mask_1 = cv2.morphologyEx(mask_1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8), iterations = 2)
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE,np.ones((3,3),np.uint8), iterations = 1)
    # Combining the masks and showing them in one frame
    mask_2 =cv2.bitwise_not(mask_1)
    result1 = cv2.bitwise_and(background,background,mask=mask_1)

#The basic work of bitwise_and is to combine these background and store it in result1
    result2 = cv2.bitwise_and(img,img,mask=mask_2)
    final_output = cv2.addWeighted(result1,1,result2,1,0)
    cv2.imshow('Cloak of Invisibility',final_output)
    k = cv2.waitKey(10)
    # To quit the program user can press Escape key ( 27 is the ASCII Code for Escape)
    if k==27:
        break
cap.release()
cv2.destroyAllWindows()

