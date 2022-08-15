import os
import cv2 as cv

class Loader:
    def __init__(self, capture, idx):
        self.idx = idx

    @staticmethod
    async def sort_slides(path: str):
        slides = os.listdir(path)
        # sorting to be implemented here
        return slides

    @staticmethod
    async def load_slide(idx: int, sorted: list):
        slides = sorted
        path = f'./data/imgs/{slides[idx]}'
        slide = cv.imread(path)
        return slide