import cv2
import mediapipe as mp
import pyautogui
import mouse
import numpy as np
import time
import math

video = cv2.VideoCapture(1)
pozicija = [[0,0]]
index = 0
alpha = 1

handGesture = mp.solutions.hands.Hands()
drawingTools = mp.solutions.drawing_utils
screenWidth, screenHeight = pyautogui.size()
while True:
   kaziprst = False
   srednji = False
   domali = False
   mali = False
   desna = False
   lijeva = False
   _, frame = video.read()
   frameR = 150
   frame = cv2.flip(frame, 1)
   frame = cv2.resize(frame, (600,600))
   frameHeight, frameWidth, _ = frame.shape
   #rec = cv2.rectangle(frame, (frameR, frameR), (frameHeight - frameR, frameWidth-frameR), (255,0,0), 2)
   rgbConvertedFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   output = handGesture.process(rgbConvertedFrame)
   hands = output.multi_hand_landmarks
   frame.flags.writeable = False
   fingerCount = 0          
   if hands:  
       for hand in hands:
           handIndex = output.multi_hand_landmarks.index(hand)
           handLabel = output.multi_handedness[handIndex].classification[0].label
           handLandmarks = []
           drawingTools.draw_landmarks(frame, hand)
           landmarks = hand.landmark
           for id, landmark in enumerate(landmarks):
               handLandmarks.append([landmark.x, landmark.y])
               if id == 9:
                x = int(landmark.x*frameWidth)
                y = int(landmark.y*frameHeight)
                cv2.circle(img=frame, center=(x,y), radius=15, color=(0, 255, 255))
                cx_new = int(np.interp(x, (frameR, frameWidth - frameR ), (0, 2048)))
                cy_new = int(np.interp(y, (frameR, frameHeight - frameR ), (0, 1152)))
                if cx_new > pozicija[index][0] + alpha and cy_new > pozicija[index][1] + alpha:
                  mouse.move(cx_new, cy_new)
                elif cx_new < pozicija[index][0] - alpha and cy_new < pozicija[index][1] - alpha:
                   mouse.move(cx_new, cy_new)
                elif cx_new > pozicija[index][0] + alpha and cy_new < pozicija[index][1] - alpha:
                   mouse.move(cx_new, cy_new)
                elif cx_new < pozicija[index][0] - alpha and cy_new > pozicija[index][1] + alpha:
                   mouse.move(cx_new, cy_new)
                pozicija.append([cx_new, cy_new])
                index += 1                    
           if handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]:
               fingerCount = fingerCount+1
               lijeva = True
           elif handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]:
               fingerCount = fingerCount+1
               desna = True
           if handLandmarks[8][1] < handLandmarks[6][1]:       #kaziprst
             fingerCount = fingerCount+1
             kaziprst = True
           if handLandmarks[12][1] < handLandmarks[10][1]:     #srednji
             fingerCount = fingerCount+1
             srednji = True
           if handLandmarks[16][1] < handLandmarks[14][1]:     #domali
             fingerCount = fingerCount+1
             domali = True
           if handLandmarks[20][1] < handLandmarks[18][1]:     #Pinky
             fingerCount = fingerCount+1
             mali = True
           if kaziprst == True and desna == False and srednji == True and domali == True and mali == True:
              mouse.click()
              time.sleep(0.1)
              continue
           if kaziprst == True and srednji == True and desna == True and domali == False and mali == True:
              mouse.double_click()
              continue
           if kaziprst == True and srednji == True and desna == True and domali == True and mali == False:
              mouse.right_click()
              continue
           if kaziprst == False and srednji == True and desna == True and domali == True and mali == True:
              if mouse.get_position()[1] < 576:
                 mouse.wheel(1)
              elif mouse.get_position()[1] > 576:
                 mouse.wheel(-1)
              





   cv2.imshow('Virtual Mouse', frame)
   cv2.waitKey(1)



#frame je x650,y500
#plavakutija x1 = 100, y1 = 100
#140,540 = x 400
#100,400 = y 300