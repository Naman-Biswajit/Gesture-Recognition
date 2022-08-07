import os
import asyncio
import cv2 as cv

from dotenv import load_dotenv
from core.slides import Loader


current_slide = 0
run = True

load_dotenv()
camera_index = int(os.environ.get('CAMERA_INDEX'))
cam_x = int(os.environ.get('INTEGRATED_FRAME_X'))
cam_y = int(os.environ.get('INTEGRATED_FRAME_Y'))

capture = cv.VideoCapture(camera_index)
capture.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

async def main():
    global run

    while run:

        slide = await Loader.load_slide(current_slide)
        matrix = slide.shape

        status, frame = capture.read()
        integrated_frame = cv.resize(frame, (cam_x, cam_y))
        
        x, y, z = matrix
        print(matrix)
        slide[0:cam_y, x - cam_x:x] = integrated_frame
        
        if status:
            cv.imshow('IT-EXHIBITION', slide)
            cv.imshow('Camera View', frame)

        else:
            print('Error: Cannot read frame')

        if cv.waitKey(1) == ord('q'):
            run = False
            capture.release()
            cv.destroyAllWindows()


if __name__ == '__main__':
    asyncio.run(main())