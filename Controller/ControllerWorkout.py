import Constants as cons
import Extensions as extn
from Controller.ControllerTraining import ControllerTraining
from Model.ModelTraining import ModelTraining

class ControllerWorkout(ControllerTraining):
    """
    Responsible for the workout logic
    """
    def __init__(self):
        super().__init__()
        # For now we have only two training types: 'yoga'->True, and 'workout'->False
        self.tng = ModelTraining(type=False)
        self.dir = cons.dir_workout
        # Set background video with coach
        self.cap_backgrd = extn.setup_video(self.dir, self.tng.exercise.name)
        super().set_tng_timings()
    
    def run(self):
        if self.tng_active and not self.paused: 
            super().run()
        