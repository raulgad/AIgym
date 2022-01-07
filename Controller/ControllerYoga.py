
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
        # For now we have only two training types: 'yoga'->True, and 'workout'->False
        self.tng = ModelTraining(type=True)
        self.dir = cons.dir_yoga
        # Set background video with coach
        self.cap_backgrd = extn.setup_video(cons.dir_yoga, self.tng.exercise.name)
        # Set timings
        self.timer_pose = Timing()
        self.set_pose_timings()
        
        self.time_left_tng = self.tng.duration
        self.bttn_pause_fill_step = self.view.bttn_pause.width / self.tng.duration
        self.view.bttn_pause.filled_less_one = self.bttn_pause_fill_step
    
    def set_pose_timings(self):
        if self.tng.exercise:
            self.time_left_pose =  self.tng.exercise.duration
            self.time_exer_state = self.tng.exercise.state.duration
            self.bttn_next_fill_step = self.view.bttn_next.width / self.tng.exercise.duration
            self.view.bttn_next.filled_less_one = self.bttn_next_fill_step

    def run(self):
        if self.tng_active and not self.paused: 
            super().run()
            # Handle when user states in correct pose
            if self.is_corr_pose:
                if self.time_left_pose > 0:
                    # Update background of 'bttn_next' each second
                    if self.timer_pose.ticker():
                        self.time_left_pose -= 1
                        self.view.fill_background(self.view.bttn_next, self.bttn_next_fill_step)
                # Handle when pose time is end
                else:
                    self.set_pose_timings()
