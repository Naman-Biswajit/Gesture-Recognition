import pyautogui as pag
import logging
from time import time
from numpy import interp


class Handler:
    def __init__(self, config):
        self.cfg = config
        self.rx, self.ry = pag.size()
        if self.cfg.logging:
            logging.basicConfig(format=self.cfg.log_format, filename='logs.log',
                                encoding='utf-8', level=logging.INFO, filemode=self.cfg.log_mode)
        pag.FAILSAFE = False

    def cursor(self, lm_list):
        if len(lm_list) != 0:
            ix, iy = lm_list[8][1:]
            mx, my = lm_list[12][1:]
            x = interp(ix, (self.cfg.lof, self.cfg.width -
                       self.cfg.rof), (0, self.rx))
            
            y = interp(iy, (self.cfg.tof, self.cfg.height -
                       self.cfg.dof), (0, self.ry))

            pag.moveTo(x, y, _pause=False)
            return x, y

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
