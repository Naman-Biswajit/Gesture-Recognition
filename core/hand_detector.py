import cv2 as cv
from .utils import fetch_asdict_model
from mediapipe import solutions
from math import hypot

class Detector:

    def __init__(self, config):
        model = fetch_asdict_model()
        self.cfg = config
        self.mp_hands = solutions.hands
        self.hands = self.mp_hands.Hands(**model)
        self.mp_draw = solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lm_list = []

        self.styles = solutions.drawing_styles
        self.landmark_drawing_spec = self.mp_draw.DrawingSpec(
            color=(158, 46, 109), thickness=4, circle_radius=3)
        self.connection_drawing_spec = self.mp_draw.DrawingSpec(
            color=(0, 246, 255), thickness=4)

    def locate_hands(self, frame, draw=True, flip=True):
        frame_RGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(frame_RGB)
        all_hands = []
        h, w, c = frame.shape
        if self.results.multi_hand_landmarks:
            for hand_type, hand_lms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                _hand_ = {}
                _lm_list_ = []
                x_list = []
                y_list = []
                for id, lm in enumerate(hand_lms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    _lm_list_.append([px, py, pz])
                    x_list.append(px)
                    y_list.append(py)

                xmin, xmax = min(x_list), max(x_list)
                ymin, ymax = min(y_list), max(y_list)
                boxw, boxh = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxw, boxh
                cx, cy = bbox[0] + \
                    round(bbox[2] / 2), bbox[1] + round(bbox[3] / 2)

                _hand_['lm_list'] = _lm_list_
                _hand_['bbox'] = bbox
                _hand_['center'] = (cx, cy)

                if flip:
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
                                 self.cfg._bx_, 2)
                    cv.putText(frame, _hand_['type'], (bbox[0] - 30, bbox[1] - 30), cv.FONT_HERSHEY_SIMPLEX,
                               2, self.cfg._tx_, 3)

        return all_hands, frame

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

    def position(self, frame, idx=0):

        lm_list = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[idx]
            for id, lm in enumerate(hand.landmark):
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])

        return lm_list


    def distance(self, l1, l2, frame, lm_list, draw=True):
        x1, y1 = lm_list[l1][1:]
        x2, y2 = lm_list[l2][1:]
        cx, cy = round((x1 + x2)/2), round((y1 + y2)/2)

        if draw:
            cv.line(frame, (x1, y1), (x2, y2), self.cfg.circle_clr, self.cfg.thickness)
            cv.circle(frame, (x1, y1), self.cfg.radii, self.cfg.circle_clr, cv.FILLED)
            cv.circle(frame, (x2, y2), self.cfg.radii, self.cfg.circle_clr, cv.FILLED)
            cv.circle(frame, (cx, cy), self.cfg.radii-8, self.cfg.mid_clr, cv.FILLED)
        length = hypot(x2 - x1, y2 - y1)

        return length, frame, [x1, y1, x2, y2, cx, cy]
