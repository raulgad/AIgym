from Controller.ControllerTraining import ControllerTraining
import Constants as cons
import Extensions as extn

class ControllerWorkout(ControllerTraining):
    """
    Responsible for the workout logic
    """
    def __init__(self):
        super().__init__()
        self.cap_backgrd = None
        # Set background video
        self.cap_backgrd = extn.setup_video(cons.dir_workout, 'arms')
        