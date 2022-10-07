import asyncio
import logging
import cv2 as cv
import pyautogui as pygui

from core.hand_detector import Detector
from core.utils import Config


config = Config()
detector = Detector()
capture = cv.VideoCapture(config.camera_index)

capture.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv.CAP_PROP_FRAME_HEIGHT, 720)


logging.basicConfig(format=config.log_format, filename='logs.log',
                    encoding='utf-8', level=logging.INFO, filemode=config.log_mode)


async def main():
    post_action = [False, config.delay+1]
    run = True

    while run:

        status, frame = capture.read()
        frame = cv.flip(frame, 1)
        detected, frame = await detector.find_hands(frame, flipType=False)

        if config.gen_line:
            cv.line(frame, (0, config.thres_active),
                    (1280, config.thres_active), (0, 255, 0), 2)

        if detected:
            hand = detected[0]
            fingers = await detector.fingers_up(hand)
            fingers.reverse() if config.dominant_hand == 'left' else None

            print(fingers)

            _, cy = hand['center']

            if cy <= config.thres_active and post_action[1] > config.delay:
                match fingers:
                    case [1, 0, 0, 0, 0]:
                        print('\033[91m{}\033[00m'.format(
                            log := 'ACTION: Left'))
                        pygui.press('left')

                    case [0, 0, 0, 0, 1]:
                        print('\033[91m{}\033[00m'.format(
                            log := 'ACTION: Right'))
                        pygui.press('right')

                    case [0, 1, 1, 1, 0]:
                        print('\033[92m{}\033[00m'.format(
                            log := 'ACTIVE: Mouse Mode'))

                    case _:
                        log = None

                if log is not None:
                    post_action = [True, 0]
                    logging.info(log)

        if status:
            cv.imshow('Camera View', frame)

        else:
            raise Exception('Error: Cannot read frame')

        if cv.waitKey(1) == ord('q'):
            run = False
            capture.release()
            cv.destroyAllWindows()

        post_action[1] += 1 if post_action[0] else 0
        post_action[0] = False if post_action[1] > config.delay else post_action[0]

if __name__ == '__main__':
    asyncio.run(main())
