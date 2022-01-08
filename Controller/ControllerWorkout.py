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
        self.set_reps_views()
    
    def set_reps_views(self):
        self.bttn_next_fill_step = self.view.bttn_next.width / (self.tng.exercise.reps + 1)
        self.view.bttn_next.filled_less_one = self.bttn_next_fill_step

    def run(self):
        if self.tng_active and not self.paused:
            super().run()
            # Fill next button background according to exercise repetitions
            if self.tng.exercise:
                if self.done_exer_states and not self.done_exer_reps:
                    self.view.fill_background(self.view.bttn_next, self.bttn_next_fill_step)
                if self.done_exer_reps: self.set_reps_views()
                