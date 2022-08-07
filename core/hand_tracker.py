import os
import asyncio
import cv2 as cv
import mediapipe as mp

from dotenv import load_dotenv


# create a hand tracking module

class Tracker:
    def __init__(self, detection_confidence, tracking_confidence, max: int = 1, static: bool = False) -> object:
        self.static = static
        self.max = max
        self.detect_cfdce = detection_confidence
        self.track_cfdce = tracking_confidence

        self.mp_solution = mp.solutions.hands
        self.hands = self.mp_solution.Hands(
            static, max, detection_confidence, tracking_confidence)
        self.mp_drawing_utils = mp.solutions.drawing_utils


    async def detect_position(self, frame, hand_idx : int = 0, draw: bool = True, colour : tuple = (255, 255, 0)) -> tuple:
        lms = []

        if self.results.multi_hand_landmarks:
            _hand = self.results.multi_hand_landmark[hand_idx]

            for id, lm in enumerate(_hand.landmark):
                _x, _y, _z = frame.shape
                x, y = int(lm.x * _x), int(lm.y * _y)
                lms.append([id, x, y])

                if draw:
                    cv.Circle(frame, (x, y), 15, (colour), cv.FILLED)

        return lms

    async def detect_hands(self, frame, draw : bool = True):
        _frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(_frame)

        if self.results.multi_hand_landmarks:
            for hand_lm in self.results.multi_hand_landmark:
                if draw:
                    self.mp_drawing_utils.draw_hand_landmarks(frame, hand_lm, self.mp_solution.HANDS_CONNECTIONS) 
        
        return frame
