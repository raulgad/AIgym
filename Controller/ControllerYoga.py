
import Constants as cons
import Extensions as extn
from Timing import Timing
from Controller.ControllerTraining import ControllerTraining
from Model.ModelTraining import ModelTraining

class ControllerYoga(ControllerTraining):
    """
    Responsible for yoga logic
    """
    def __init__(self):
        super().__init__()
        # Set background video with coach
        self.cap_backgrd = extn.setup_video(cons.dir_yoga, 't')
        # For now we have only two trainings types: 'yoga'->True, and 'workout'->False
        self.tng = ModelTraining(type=True)
        self.time_left_tng = self.tng.duration
        self.time_left_pose =  self.tng.exercise.duration
        # Setup button's background filled parts
        self.bttn_pause_fill_step = self.view.bttn_pause.width / self.tng.duration
        self.bttn_next_fill_step = self.view.bttn_next.width / self.tng.exercise.duration
        self.view.bttn_pause.filled_less_one = self.bttn_pause_fill_step
        self.view.bttn_next.filled_less_one = self.bttn_next_fill_step
        self.timer_pose = Timing()

    def run(self):
        if self.tng_active and not self.paused: 
            super().run()

            # Handle pose timing
            if self.time_left_pose > 0:
                # Check if one second has passed
                if self.timer_pose.ticker():
                    self.time_left_pose -= 1
                    self.view.fill_background(self.view.bttn_next, self.bttn_next_fill_step)
            # Handle when pose time is end
            else:
                self.view.bttn_next.filled_width = self.view.bttn_next.width
