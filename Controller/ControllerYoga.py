import json
import os
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

        with open(os.path.join(os.path.dirname(__file__), cons.file_training), 'r') as fp:
            self.data = ModelTraining(json.load(fp))
            # print(self.data['yoga']['first']['t']['start']['angles'][(16, 14, 12)])

        # Set durations
        self.data
        duration_trng = 7 # * 60 # mins, secs
        duration_pose = 10
        self.time_left_trng = duration_trng
        self.time_left_pose = duration_pose
        # Setup button's background filled parts
        self.bttn_pause_fill_step = self.view.bttn_pause.width / duration_trng
        self.bttn_next_fill_step = self.view.bttn_next.width / duration_pose
        self.view.bttn_pause.filled_less_one = self.bttn_pause_fill_step
        self.view.bttn_next.filled_less_one = self.bttn_next_fill_step
        self.timer_pose = Timing()

    def run(self):
        if self.training_active and not self.paused: 
            self.train_timing()

            # Handle pose timing
            if self.time_left_pose > 0:
                # Check if one second has passed
                if self.timer_pose.ticker():
                    self.time_left_pose -= 1
                    self.view.fill_background(self.view.bttn_next, self.bttn_next_fill_step)
            # Handle when pose time is end
            else:
                self.view.bttn_next.filled_width = self.view.bttn_next.width
