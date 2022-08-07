import os
import cv2 as cv

class Loader:
    def __init__(self, capture, idx):
        self.capture = capture
        self.idx = idx

    def sort_slides(self):
        slides = os.listdir('./data/imgs/')
        # sorting to be implemented here
        return slides

    @staticmethod
    async def load_slide(idx: int, name: str):
        slides = Loader.sort_slides(idx)
        path = f'./data/imgs/{slides[idx]}'
        cv.imshow('IT-EXHIBITION', cv.imread(path))
        return (slides[idx], path)