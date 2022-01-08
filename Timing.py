import time

class Timing:
    """
    Responsible timing
    """
    def __init__(self):
        self.prev_time = 0
    
    def ticker(self, tm=5, value=1):
        if time.localtime(time.time() - self.prev_time)[tm] >= value:
            self.prev_time = time.time()
            return True
            