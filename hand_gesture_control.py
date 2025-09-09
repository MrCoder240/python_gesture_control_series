import cv2 #importing the OpenCV library.
from cvzone.HandTrackingModule import HandDetector #importing the HandDetector class from cvzone library.
import pyautogui#importing the pyautogui library to simulate keyboard key presses.  

detector=HandDetector(detectionCon=0.3,maxHands=2) #detectionCon is the minimum detection confidence.
                                                   #maxHands is the maximum number of hands to detect.

cam=cv2.VideoCapture(0) #0 is the index of the inbuilt webcam.

cam.set(3,640) #width.
cam.set(4,480) #height.


while True: #infinite loop to continuously capture frames from the webcam.
    success, frame=cam.read() #returns a boolean(success) if the camera is capturing or not.
                               #The frame variable stores the current image captured from the webcam.

    img=cv2.flip(frame,1) #flipping the frame horizontally for a mirror-like effect.

    hand, img=detector.findHands(img) #detecting hands in the frame and drawing landmarks on the hands.
                                       #hands is a list of detected hands with their landmarks and bounding boxes.
                                         
    if hand and hand[0]['type']=='Right': #checking if a hand is detected and if it's the right hand.
        fingers=detector.fingersUp(hand[0]) #returns a list of 5 values (0 or 1) indicating which fingers are up.
        totalFingers=fingers.count(1) #counting the number of fingers that are up.

        cv2.putText(img,f'Fingers: {totalFingers}',(50,50),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0))#displaying the count of fingers on the frame.

        if totalFingers==5:
            pyautogui.keyDown('right') #simulating the 'right' arrow key press.
            pyautogui.keyUp('left') #simulating the 'left' arrow key release.

        if totalFingers==0:
            pyautogui.keyDown('left') #simulating the 'left' arrow key press.
            pyautogui.keyUp('right') #simulating the 'right' arrow key release

    cv2.imshow("Webcam",img)#displaying the captured frame in a window named "Webcam".
    cv2.waitKey(1) #wait for 1 millisecond before moving to the next frame.
