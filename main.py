from email.policy import default
import os
import asyncio
import cv2 as cv
import pyautogui as pygui

from dotenv import load_dotenv
from core.hand_detector import Detector

load_dotenv()

camera_index = int(os.environ.get('CAMERA_INDEX'))
gen_line = eval(os.environ.get('GENERATE_LINE'))    
delay = int(os.environ.get('DELAY'))
thres_active = eval(os.environ.get('THRESHOLD_ACTIVATE'))
dominant_hand = str(os.environ.get('DOMINANT_HAND'))

async def setup():
    global camera_index
    return cv.VideoCapture(camera_index), Detector()

capture, detector = asyncio.run(setup())

capture.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv.CAP_PROP_FRAME_HEIGHT, 720)


async def main():
    post_action = [False, delay+1]
    run = True 
    
    while run:

        status, frame = capture.read()
        matrix = frame.shape

        frame = cv.flip(frame, 1)
        detected, frame = await detector.find_hands(frame, flipType=False)

        if gen_line:
            cv.line(frame, (0, thres_active), (1280, thres_active), (0, 255, 0), 2)

        if detected:
            hand = detected[0]
            fingers = await detector.fingers_up(hand)
            fingers.reverse() if dominant_hand == 'left' else None

            print(fingers)

            _, cy = hand['center']

            if cy <= thres_active and post_action[1] > delay:
                match fingers:
                    case [1, 0, 0, 0, 0]:
                        print('ACTION: LEFT')
                        pygui.press('left')
                        post_action = [True, 0]

                    case [0, 0, 0, 0, 1]:
                        print('ACTION: RIGHT')
                        pygui.press('right')
                        post_action = [True, 0]
                    
        if status:
            cv.imshow('Camera View', frame)

        else:
            print('Error: Cannot read frame')

        if cv.waitKey(1) == ord('q'):
            run = False
            capture.release()
            cv.destroyAllWindows()

        post_action[1] += 1 if post_action[0] else 0
        post_action[0] = False if post_action[1] > delay else post_action[0]

if __name__ == '__main__':
    asyncio.run(main())
