from threading import Thread


class Threader:
    def __init__(self, config):
        self.config = config

    def run(self, func, *args, is_daemon: bool = True) -> Thread:
        thread = Thread(target=func, args=args)
        thread.daemon = is_daemon
        thread.start()
        return thread

    def wait_util_complete(self, *args) -> tuple:
        for thread in args:
            thread.join()
        
        return(args)
