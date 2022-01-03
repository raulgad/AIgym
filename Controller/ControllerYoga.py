from Controller.ControllerTrain import ControllerTrain
import Constants as cons
import Extensions as extn

class ControllerYoga(ControllerTrain):
    """
    Responsible for the yoga logic
    """
    def __init__(self):
        super().__init__()
        self.cap_backgrd = None
        # Set background video
        self.cap_backgrd = extn.setup_video(cons.dir_yoga, 't')