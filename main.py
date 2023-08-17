import cv2 as cv
import time

from core.hand_detector import Detector
from core.utils import Config
from core.event_handler import Handler

config = Config()
handle = Handler()
detector = Detector(config)

capture = cv.VideoCapture(config.camera_index)
capture.set(cv.CAP_PROP_FRAME_WIDTH, config.width)
capture.set(cv.CAP_PROP_FRAME_WIDTH, config.height)

def main():
    post_action = [False, config.delay+1]
    run = True

    while run:
        t1 = time.time()
        _, frame = capture.read()
        frame = cv.flip(frame, 1)

        detected, frame = detector.locate_hands(frame, flipType=False)

        if config.gen_box:
            x, y = config.thres_x, config.thres_y
            overlay = frame.copy()
            cv.rectangle(overlay, (config.width, 0),
                         (config.width - x, y), config.field_clr, -1)
            frame = cv.addWeighted(
                overlay, config.field_opacity, frame, 1-config.field_opacity, 0)

        if detected:
            hand = detected[0]
            fingers = detector.fingers_up(hand)

            print(fingers)

            x, y = hand['center']
            flag = y <= config.thres_y and x >= config.width - config.thres_x
            if flag and post_action[1] > config.delay:
                post_action = handle.fingers(fingers, post_action)

        post_action[1] += 1 if post_action[0] else 0
        post_action[0] = False if post_action[1] > config.delay else post_action[0]

        t2 = time.time()
        fps = 1/float(t2-t1)

        cv.putText(frame, f"FPS: {round(fps)}", (50, 50),
                   cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv.imshow('Camera View', frame)

        if cv.waitKey(1) == ord('q'):
            run = False
            capture.release()
            cv.destroyAllWindows()


if __name__ == '__main__':
    main()