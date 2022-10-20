import pyautogui as pygui


class Control:
    def __init__(self, config):
        self.config = config
        self.resolution = pygui.size()

    def mouse(self):
        pass
