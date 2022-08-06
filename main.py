import os
import asyncio
import cv2 as cv

from dotenv import load_dotenv


load_dotenv()
capture = cv.VideoCapture(os.environ.get('CAMERA_INDEX'))
capture.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv.CAP_PROP_FRAME_HEIGHT, 720)



async def main():
    status, frame = capture.read()
    
    if status:
        cv.imshow('Test', frame)
        cv.waitKey(1)

if __name__ == '__main__':
    asyncio.run(main())