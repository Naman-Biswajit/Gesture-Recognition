import cv2
import mediapipe as mp


class Detector():
    def __init__(self, mode=False, max_hands=1, model_complexity=1, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.model_complexity = model_complexity
        self.detection_con = detection_con
        self.track_con = track_con
        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.model_complexity,
                                         self.detection_con, self.track_con)

        self.mp_draw = mp.solutions.drawing_utils

    async def find_position(self, frame, hand_no=0, draw=True, colour=(255, 0, 250)):

        lm_list = []
        if self.results.multi_hand_landmarks:
            __hand__ = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(__hand__.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(frame, (cx, cy), 15, colour, cv2.FILLED)

        return lm_list

    async def find_hands(self, frame, draw=True):
        frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frame_RGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(frame, handLms,
                                               self.mp_hands.HAND_CONNECTIONS)
        return frame
