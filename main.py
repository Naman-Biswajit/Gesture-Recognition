import os
import asyncio
import cv2 as cv

from dotenv import load_dotenv
from core.Slides import Loader

load_dotenv()
camera_index = int(os.environ.get('CAMERA_INDEX'))
run = True
current_slide = 0

capture = cv.VideoCapture(camera_index)
capture.set()

async def main():
    global run

    while run:
        await Loader.load_slide(current_slide, 'IT-Exhibition')
        status, frame = capture.read()

        if status:
            cv.imshow('Camera View', frame)
            cv.waitKey(1)

        else:
            print('Error: Cannot read frame')

        if cv.waitKey(1) == ord('q'):
            run = False
            capture.release()
            cv.destroyAllWindows()


if __name__ == '__main__':
    asyncio.run(main())