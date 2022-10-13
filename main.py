import asyncio
import logging
import cv2 as cv
import pyautogui as pygui
import time

from core.hand_detector import Detector
from core.utils import Config


config = Config()
detector = Detector()
capture = cv.VideoCapture(config.camera_index)

capture.set(cv.CAP_PROP_FRAME_WIDTH, m_x := 1280)
capture.set(cv.CAP_PROP_FRAME_HEIGHT, m_y := 720)


if config.logging:
    logging.basicConfig(format=config.log_format, filename='logs.log',
                        encoding='utf-8', level=logging.INFO, filemode=config.log_mode)


def main():
    post_action = [False, config.delay+1]
    run = True

    while run:
        t1 = time.time()
        status, frame = capture.read()
        frame = cv.flip(frame, 1)
        detected, frame = detector.find_hands(frame, flipType=False)

        if config.gen_box:
            x, y = config.thres_x, config.thres_y
            overlay = frame.copy()
            cv.rectangle(overlay, (m_x, 0), (m_x - x, y), config.field_clr, -1)
            frame = cv.addWeighted(
                overlay, config.field_opacity, frame, 1-config.field_opacity, 0)

        if detected:
            hand = detected[0]
            fingers = detector.fingers_up(hand)
            # fingers.reverse() if config.dominant_hand == 'left' else None

            print(fingers)

            x, y = hand['center']
            flag = y <= config.thres_y and x >= m_x - config.thres_x
            if flag and post_action[1] > config.delay:
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

                    case [0, 1, 1, 1, 1]:
                        print("\033[1m\033[31m{}\033[0m".format(
                            log := 'TOGGLE: Assist Box'))
                        config.gen_box = not config.gen_box

                    case _:
                        log = None

                if log is not None:
                    post_action = [True, 0]
                    logging.info(log) if config.logging else None

        post_action[1] += 1 if post_action[0] else 0
        post_action[0] = False if post_action[1] > config.delay else post_action[0]

        t2 = time.time()
        fps = 1/float(t2-t1)

        cv.putText(frame, f"FPS: {fps:.2f}", (50, 50),
                   cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv.imshow('Camera View', frame)

        if cv.waitKey(1) == ord('q'):
            run = False
            capture.release()
            cv.destroyAllWindows()

if __name__ == '__main__':
    main()
