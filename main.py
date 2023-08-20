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
        
        self.move = True
        self.lx, self.ly = 0, 0
        
        self.main()

    def overaly_field(self, frame):
        if self.cfg.G_field:
            x, y = self.cfg.tx, self.cfg.ty
            overlay = frame.copy()
            cv.rectangle(overlay, (self.cfg.width, 0),
                         (self.cfg.width - x, y), self.cfg.field_clr, -1)
            frame = cv.addWeighted(
                overlay, self.cfg.field_opacity, frame, 1-self.cfg.field_opacity, 0)

        return frame

    def process(self, detected, lm_list):
        cordinates = [-100, -100, -100, -100]

        if detected:
            hand = detected[0]
            fingers = self.detector.fingers_up(hand)

            print(fingers)

            x, y = hand['center']
            flag = y <= self.cfg.ty and x >= self.cfg.width - self.cfg.tx

            if self.move:
                delta = (self.lx, self.ly)
                cordinates = self.event.cursor(lm_list, delta)
            
            elif flag:
                self.td = self.event.execute(fingers, self.td, lm_list)

        return cordinates

    def generate_region(self, frame, cord):

        if cord[0] >= 0 and cord[1] >= 0:
            cv.rectangle(frame,
                         (self.cfg.lof, self.cfg.tof),
                         (self.cfg.width-self.cfg.rof,
                          self.cfg.height-self.cfg.dof),
                          self.cfg.rect_clr,
                          self.cfg.thickness)
            
            cv.circle(frame, (cord[2], cord[3]), self.cfg.radii, self.cfg.circle_clr, cv.FILLED)
        
        return frame

    def main(self):
        run = True
        self.td = 0

        while run:
            t1 = time.time()
            _, frame = self.capture.read()
            frame = cv.flip(frame, 1)

            detected, frame = self.detector.locate_hands(frame, flip=False)
            frame = self.overaly_field(frame) if self.move else frame

            lm_list = self.detector.position(frame)
            cordinates = self.process(detected, lm_list)
            frame = self.generate_region(frame, cordinates)

            self.lx, self.ly = cordinates[0], cordinates[1]
            frame = self.event.click(self.detector, frame, lm_list)


            t2 = time.time()
            fps = 1/float(t2-t1)

            cv.putText(frame, f"FPS: {round(fps)}", (50, 50),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

            cv.imshow('Camera View', frame)

            if cv.waitKey(1) == ord('q'):
                run = False
                self.capture.release()
                cv.destroyAllWindows()

            if cv.waitKey(1) == ord('m'):
                print('TOGGLE: Mouse Mode')
                self.move = not self.move

if __name__ == '__main__':
    VideoStream()
