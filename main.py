import cv2 as cv
import time

from core.hand_detector import Detector
from core.utils import Config
from core.event_handler import Handler


class VideoStream:
    def __init__(self) -> None:
        self.cfg = Config()
        self.event = Handler(self.cfg)
        self.detector = Detector(self.cfg)

        self.capture = cv.VideoCapture(self.cfg.camera_index)
        self.capture.set(cv.CAP_PROP_FRAME_WIDTH, self.cfg.width)
        self.capture.set(cv.CAP_PROP_FRAME_WIDTH, self.cfg.height)
        self.main()

    def overaly_field(self, frame):
        if self.cfg.G_field:
            x, y = self.cfg.thres_x, self.cfg.thres_y
            overlay = frame.copy()
            cv.rectangle(overlay, (self.cfg.width, 0),
                        (self.cfg.width - x, y), self.cfg.field_clr, -1)
            frame = cv.addWeighted(
                overlay, self.cfg.field_opacity, frame, 1-self.cfg.field_opacity, 0)
            
        return frame
     
    def process(self, detected, post_action):
        if detected:
            hand = detected[0]
            fingers = self.detector.fingers_up(hand)

            print(fingers)

            x, y = hand['center']
            flag = y <= self.cfg.thres_y and x >= self.cfg.width - self.cfg.thres_x
            
            if flag and post_action[1] > self.cfg.delay:
                post_action = self.event.fingers(fingers, post_action)
        return post_action

    def main(self):
        post_action = [False, self.cfg.delay+1]
        run = True

        while run:
            t1 = time.time()
            _, frame = self.capture.read()
            frame = cv.flip(frame, 1)

            detected, frame = self.detector.locate_hands(frame, flipType=False)
            frame = self.overaly_field(frame)

            post_action = self.process(detected, post_action)

            post_action[1] += 1 if post_action[0] else 0
            post_action[0] = False if post_action[1] > self.cfg.delay else post_action[0]

            t2 = time.time()
            fps = 1/float(t2-t1)

            cv.putText(frame, f"FPS: {round(fps)}", (50, 50),
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

            cv.imshow('Camera View', frame)

            if cv.waitKey(1) == ord('q'):
                run = False
                self.capture.release()
                cv.destroyAllWindows()


if __name__ == '__main__':
    VideoStream()