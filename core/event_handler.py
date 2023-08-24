import os
import sys
import subprocess
import pyautogui as pag
import logging

from time import time, sleep
from numpy import interp



class Handler:
    def __init__(self, config):
        self.cfg = config
        self.rx, self.ry = pag.size()

        self.hold_time, self.change_time = 0, 0
        self.hold, self.change = False, False
        
        if self.cfg.logging:
            logging.basicConfig(format=self.cfg.log_format, filename='logs.log',
                                encoding='utf-8', level=logging.INFO, filemode=self.cfg.log_mode)
        pag.FAILSAFE = False

    def open_file(self, filename: str):
        if sys.platform == "win32":
            os.startfile(filename)

        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])
        
        sleep(0.1)
        pag.hotkey('winleft', 'left')

    def cursor(self, lm_list, delta):
        if len(lm_list) != 0:
            lx, ly = delta
            ix, iy = lm_list[8][1:]
            u = interp(ix, (self.cfg.lof, self.cfg.width -
                       self.cfg.rof), (0, self.rx))

            v = interp(iy, (self.cfg.tof, self.cfg.height -
                       self.cfg.dof), (0, self.ry))

            x = lx + (u-lx) / self.cfg.sensitivity
            y = ly + (v-ly) / self.cfg.sensitivity

            pag.moveTo(x, y, _pause=False)
            return [x, y, ix, iy]

    def click(self, detector, frame, lm_list, click_time):
        offset = click_time+self.cfg.click_rate

        if len(lm_list) != 0 and (t:=time()) > offset:
            length, frame, _ = detector.distance(8, 12, frame, lm_list)

            if (length < 30):
                click_time = t
                pag.click(button="primary")
                print('MOUSE: CLICKED')

        return frame, click_time
    
    def hold_action(self, fingers):
        match fingers:
            case [1, 1, 1, 1, 0]:
                if not self.hold:
                    self.hold = True
                    self.hold_time = time()
                
                else:
                    if self.cfg.hold_thres + self.hold_time < time():
                        files = os.listdir((path:='./imgs/'))
                        
                        filename = path+f if (f:='1.jpeg') in files else files[0]
                        self.open_file(filename)
                        print('OPENED FILE')
                        self.hold = False
                        self.hold_time = 0

            case _:
                self.hold = False
                
    
    def change_mode(self, fingers, move):
        match fingers:
            case [1, 0, 1, 0, 1]:
                if not self.change:
                    self.change = True
                    self.change_time = time()
                
                else:
                    if self.cfg.change_thres + self.change_time < time():
                        self.change = False
                        self.change_time = 0
                        print('MODE: CHANGED')
                        move = not move
        return move
                    
    def execute(self, fingers, timed, log=None):
        offset = timed+self.cfg.delay
        if offset < time():
            match fingers:
                case [1, 0, 0, 0, 0]:
                    print('\033[91m{}\033[00m'.format(
                        log := 'ACTION: Left'))
                    pag.press('left')
                    td = time()

                case [0, 0, 0, 0, 1]:
                    print('\033[91m{}\033[00m'.format(
                        log := 'ACTION: Right'))
                    pag.press('right')
                    td = time()

                case _:
                    td = 0

        else:
            td = timed

        if log is not None and self.cfg.logging:
            logging.info(log)

        return td
