import sys
import time
import threading

class Spinner():

    SPINNER = '|/-\\'
    BALOON = '.oO@*'
    
    busy = False
    delay = 0.5
    message = None


    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in Spinner.SPINNER: yield cursor

    def __init__(self, delay=None, message=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay
        self.message = message

    def spinner_task(self):
        while self.busy:
            sys.stdout.write("%s%s" % (self.message, next(self.spinner_generator)))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b'*(len(self.message)+1))
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False
