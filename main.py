import ctypes
import math
import time
from array import *
import numpy as np
#import tensorflow
import cv2
import mediapipe as mp
import pyautogui
#from tensorflow.keras.models import load_model

user32 = ctypes.windll.user32
resx = user32.GetSystemMetrics(0) * 1.3
resy = user32.GetSystemMetrics(1) * 1.3

pyautogui.FAILSAFE = False
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0

middleDown = False
count = 0
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
pos = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
answ = ""
def main():
    global count, answ
    oldPos = pos[5]
    cap = cv2.VideoCapture(0)
    print(cap)
    
    print("""
    This is an emulator that uses a webcam to convert a hand into a mouse.
    The controls are simple, fold your index finger to left click, fold your index finger
    twice in quick succession to hold left click, fold your ring finger to right click,
    fold your middle finger to click with the scroll wheel, touch your thumb to your pinky finger
    to see all tabs, and make a fist with your hand to exit the program. Enjoy!
    """)
    

    mp_hands = mp.solutions.hands
    cap.set(3, resx)
    cap.set(4, resy)
    start = 0
    posStart = time.perf_counter()
    posStop = time.perf_counter()
    hands = mp_hands.Hands(model_complexity=0, max_num_hands = 1, min_detection_confidence=0.7, min_tracking_confidence=0.05)
    x = 0
    while cap.isOpened():
        success, image = cap.read()
        cv2.waitKey(20)
        if not success:
            print("Error: Could not read image.")
            continue
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        image.flags.writeable = True
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            count = 0
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(), mp_drawing_styles.get_default_hand_connections_style())
            temp_landmark = hand_landmarks.landmark[5]
            findPos(hand_landmarks)
            if posStop - posStart > 0.3:
                oldPos = findPos(temp_landmark)
                posStart = posStop
            posStop = time.perf_counter()
            if not aimAssist(pos, oldPos):
                pyautogui.moveTo(pos[5][0], pos[5][1], _pause = False)
            start = checkGestures(start)
                    
        cv2.imshow('Camera', cv2.flip(image, 1))

def findCoords(landmark):
    x = landmark.x
    y = landmark.y
    x = int(math.floor((resx - (x * resx))))
    y = int(math.floor(y * resy))
    return [x, y]

def findPos(joints):
    try:
        count = 0
        for landmark in joints.landmark:
            pos[count] = findCoords(landmark)
            count += 1
    except:
        return findCoords(joints)

    

def aimAssist(pos, oldPos):
    if (oldPos[1] - pos[5][1] > 12 or oldPos[1] - pos[5][1] < -12) and (oldPos[0] - pos[5][0] > 12 or oldPos[0] - pos[5][0] < -12):
        return False
    else:
        return True
    
def checkGestures(start):
    global middleDown, answ
    stop = time.perf_counter()
    if pos[8][1] > pos[6][1] and pos[12][1] > pos[10][1] and pos[16][1] > pos[14][1] and pos[20][1] > pos[18][1]:
        pyautogui.mouseUp(button="middle")
        pyautogui.mouseUp(button='left')
        exit()

    if pos[8][1] > pos[6][1] and pos[12][1] < pos[10][1] and pos[16][1] > pos[14][1] and pos[20][1] > pos[18][1]:
        print("Rude.")

    if pos[8][1] > pos[6][1]:
        if stop - start < 0.8 and stop - start > 0:
            pyautogui.mouseDown(button='left')
        
        else:
            pyautogui.click(button='left', interval = 0.1)
            pyautogui.mouseUp(button='left')
        return time.perf_counter()

    if (pos[4][0] - pos[20][0] < 50 and pos[4][0] - pos[20][0] > -50) and (pos[4][1] - pos[20][1] < 50 and pos[4][1] - pos[20][1] > -50):
        pyautogui.hotkey("win", "tab", interval = 0.1)

    if pos[16][1] > pos[14][1]:
        pyautogui.click(button="right", interval = 0.1)

    if pos[12][1] > pos[10][1] and not middleDown:
        pyautogui.mouseDown(button="middle")
        middleDown = True
        
    if pos[12][1] > pos[10][1] and middleDown:
        pyautogui.mouseUp(button="middle")
        middleDown = False
    return start

if __name__ == "__main__":
    main()