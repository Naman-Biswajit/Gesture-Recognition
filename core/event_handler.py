import pyautogui as pag
import logging
from time import time

class Handler:
    def __init__(self, config):
        self.cfg = config
        
        if self.cfg.logging:
            logging.basicConfig(format=self.cfg.log_format, filename='logs.log',
                                encoding='utf-8', level=logging.INFO, filemode=self.cfg.log_mode)
    
    def execute(self, fingers, timed, log=None):
        offset = timed+self.cfg.delay
        if  offset < time():
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