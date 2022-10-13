import math
import cv2 as cv
import mediapipe as mp

from .utils import Config


class Detector:

    def __init__(self, static=False, max_hands=1, detection_con=0.8, min_track_con=0.5):
        self.config = Config()
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.min_track_con = min_track_con
        self.static = static
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=self.static, max_num_hands=self.max_hands,
                                         min_detection_confidence=self.detection_con,
                                         min_tracking_confidence=self.min_track_con)
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lm_list = []

        self.styles = mp.solutions.drawing_styles
        self.landmark_drawing_spec = self.mp_draw.DrawingSpec(
            color=(158, 46, 109), thickness=4, circle_radius=3)
        self.connection_drawing_spec = self.mp_draw.DrawingSpec(
            color=(0, 246, 255), thickness=4)

    def find_hands(self, frame, draw=True, flipType=True):
        frame_RGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(frame_RGB)
        all_hands = []
        h, w, c = frame.shape
        if self.results.multi_hand_landmarks:
            for hand_type, hand_lms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                _hand_ = {}
                _lm_list_ = []
                xList = []
                yList = []
                for id, lm in enumerate(hand_lms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    _lm_list_.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)

                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cx, cy = bbox[0] + (bbox[2] // 2), bbox[1] + (bbox[3] // 2)

                _hand_['lm_list'] = _lm_list_
                _hand_['bbox'] = bbox
                _hand_['center'] = (cx, cy)

                if flipType:
                    if hand_type.classification[0].label == 'Right':
                        _hand_['type'] = 'Left'
                    else:
                        _hand_['type'] = 'Right'
                else:
                    _hand_['type'] = hand_type.classification[0].label

                all_hands.append(_hand_)

                if draw:
                    self.mp_draw.draw_landmarks(frame, hand_lms,
                                                self.mp_hands.HAND_CONNECTIONS,
                                                landmark_drawing_spec=self.landmark_drawing_spec,
                                                connection_drawing_spec=self.connection_drawing_spec
                                                )
                    cv.rectangle(frame, (bbox[0] - 20, bbox[1] - 20),
                                 (bbox[0] + bbox[2] + 20,
                                  bbox[1] + bbox[3] + 20),
                                 self.config._bx_, 2)
                    cv.putText(frame, _hand_['type'], (bbox[0] - 30, bbox[1] - 30), cv.FONT_HERSHEY_SIMPLEX,
                               2, self.config._tx_, 3)
        if draw:
            return all_hands, frame
        else:
            return all_hands

    def fingers_up(self, _hand_):
        hand__type = _hand_['type']
        _lm_list_ = _hand_['lm_list']
        if self.results.multi_hand_landmarks:
            fingers = []
            if hand__type == 'Right':
                if _lm_list_[self.tip_ids[0]][0] > _lm_list_[self.tip_ids[0] - 1][0]:
                    fingers.append(0)
                else:
                    fingers.append(1)
            else:
                if _lm_list_[self.tip_ids[0]][0] < _lm_list_[self.tip_ids[0] - 1][0]:
                    fingers.append(0)
                else:
                    fingers.append(1)

            for id in range(1, 5):
                if _lm_list_[self.tip_ids[id]][1] < _lm_list_[self.tip_ids[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers

    def find_distance(self, p1, p2, frame=None):

        x1, y1 = p1
        x2, y2 = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        info = (x1, y1, x2, y2, cx, cy)
        if frame is not None:
            cv.circle(frame, (x1, y1), 15, self.config._cr_, cv.FILLED)
            cv.circle(frame, (x2, y2), 15, self.config._cr_, cv.FILLED)
            cv.line(frame, (x1, y1), (x2, y2), self.__ln__, 3)
            cv.circle(frame, (cx, cy), 15, self.cr, cv.FILLED)
            return length, info, frame
        else:
            return length, info
