import cv2 #importing the OpenCV library.
from cvzone.HandTrackingModule import HandDetector #importing the HandDetector class from cvzone library.
import pyautogui#importing the pyautogui library to simulate keyboard key presses.  

detector=HandDetector(detectionCon=0.5,maxHands=2) #detectionCon is the minimum detection confidence.
                                                   #maxHands is the maximum number of hands to detect.

cam=cv2.VideoCapture(0) #0 is the index of the inbuilt webcam.

cam.set(3,640) #width.
cam.set(4,480) #height.

# Variables to track key states
right_key_pressed = False
left_key_pressed = False

while True: #infinite loop to continuously capture frames from the webcam.
    success, frame=cam.read() #returns a boolean(success) if the camera is capturing or not.
                               #The frame variable stores the current image captured from the webcam.
    
    if not success:
        print("Failed to capture frame")
        break

    img=cv2.flip(frame,1) #flipping the frame horizontally for a mirror-like effect.

    hands, img=detector.findHands(img, flipType=False) #detecting hands in the frame and drawing landmarks on the hands.
                                       #hands is a list of detected hands with their landmarks and bounding boxes.
    
    # Reset control flags for each frame
    move_right = False
    move_left = False
                                         
    if hands: #checking if any hands are detected
        for hand in hands:
            hand_type = hand['type'] # 'Left' or 'Right'
            fingers=detector.fingersUp(hand) #returns a list of 5 values (0 or 1) indicating which fingers are up.
            totalFingers=fingers.count(1) #counting the number of fingers that are up.

            # Display finger count for each hand
            position = (50, 50) if hand_type == 'Right' else (50, 100)
            cv2.putText(img,f'{hand_type}: {totalFingers}',position,cv2.FONT_HERSHEY_PLAIN,2,(0,255,0))#displaying the count of fingers on the frame.

            # Control logic for both hands
            if totalFingers==5:
                move_right = True
            elif totalFingers==0:
                move_left = True

    # Apply controls based on hand gestures
    if move_right and not right_key_pressed:
        pyautogui.keyDown('right')
        if left_key_pressed:
            pyautogui.keyUp('left')
            left_key_pressed = False
        right_key_pressed = True
        
    elif move_left and not left_key_pressed:
        pyautogui.keyDown('left')
        if right_key_pressed:
            pyautogui.keyUp('right')
            right_key_pressed = False
        left_key_pressed = True
        
    # Release keys when no gesture is detected
    elif not move_right and right_key_pressed:
        pyautogui.keyUp('right')
        right_key_pressed = False
        
    elif not move_left and left_key_pressed:
        pyautogui.keyUp('left')
        left_key_pressed = False

    cv2.imshow("Webcam",img)#displaying the captured frame in a window named "Webcam".
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cam.release()
cv2.destroyAllWindows()

# Ensure all keys are released when program ends
if right_key_pressed:
    pyautogui.keyUp('right')
if left_key_pressed:
    pyautogui.keyUp('left')
