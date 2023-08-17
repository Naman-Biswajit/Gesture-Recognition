import pyautogui
import logging
from .utils import Config

class Handler:
    def __init__(self, ):
        self.config = Config()
        
        if self.config.logging:
            logging.basicConfig(format=self.config.log_format, filename='logs.log',
                                encoding='utf-8', level=logging.INFO, filemode=self.onfig.log_mode)
    
    def fingers(self, fingers, post_action):
        match fingers:
            case [1, 0, 0, 0, 0]:
                print('\033[91m{}\033[00m'.format(
                    log := 'ACTION: Left'))
                pyautogui.press('pageup')

            case [0, 0, 0, 0, 1]:
                print('\033[91m{}\033[00m'.format(
                    log := 'ACTION: Right'))
                pyautogui.press('pagedown')
                print('check')
           
            case _:
                log = None
                
        if log is not None:
            post_action = [True, 0]
            logging.info(log) if self.config.logging else None

        return post_action