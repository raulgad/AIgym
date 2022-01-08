import Router as router
import Constants as cons
import Extensions as extn
from Timing import Timing
from View.ViewTrain import ViewTrain
from Controller.Controller import Controller
from Controller.ControllerModalPause import ControllerModalPause

class ControllerTraining(Controller):
    """
    Responsible for the train logic
    """
    def __init__(self):
        super().__init__()
        self.dir = ''
        self.cap_backgrd = None
        self.paused = False
        self.tng = None
        self.tng_active = True
        self.is_corr_pose = False
        self.done_exer_states = False
        self.done_exer_reps = False
        # Layout train view
        self.view = ViewTrain(ctrl=self)
        # Set callbacks to train buttons actions
        self.view.bttn_pause.action = self.tap_pause
        self.view.bttn_next.action = self.tap_next
        # Setup button's background filled parts
        self.bttn_pause_fill_step = 0
        self.view.bttn_pause.filled_less_one = 0
        self.time_left_tng = 0
        self.timer_tng = Timing()
        self.time_exer_state = 0
        self.timer_exer_state = Timing()

    def tap_pause(self):
        self.paused = True
        self.view.pause_background()
        router.segue(fr=self, to=ControllerModalPause(super_ctrl=self), modal=True)

    def tap_next(self):
        if self.tng_active:
            self.tng.set_next_exercise()
            if self.tng.exercise: self.update_exercise()
            else: self.done()

    def set_tng_timings(self):
        self.time_left_tng = self.tng.duration
        self.bttn_pause_fill_step = self.view.bttn_pause.width / self.tng.duration
        self.view.bttn_pause.filled_less_one = self.bttn_pause_fill_step
        
    def done(self):
        self.tng_active = False
        self.view.done()
    
    def update_exercise(self):
        self.view.bttn_next.filled_width = 0
        self.cap_backgrd = extn.setup_video(self.dir, self.tng.exercise.name)

    def run(self):
        if self.tng_active and not self.paused:
            # Handle training timing
            if self.time_left_tng > 0:
                # Check if one second has passed
                if self.timer_tng.ticker():
                    # Update pause button view
                    self.time_left_tng -= 1
                    trng_mins, trng_secs = divmod(self.time_left_tng, 60)
                    self.view.bttn_pause.label.text = cons.lbl_pause + ' {:02d}:{:02d}'.format(trng_mins, trng_secs)
                    self.view.fill_background(self.view.bttn_pause, self.bttn_pause_fill_step)
            # Handle when training time is end
            else:
                self.tng_active = False
                self.view.tng_time_end()
            # Detect pose
            incorr_angs = self.tng.incorr_angs(self.tng.exercise.state.angles)
            self.is_corr_pose = not incorr_angs
            # Update view according to analyzed pose
            self.view.draw_corrections(incorr_angs)
            self.view.update_label(self.tng.exercise.name, self.is_corr_pose)
            # Handle when user stands in correct pose
            if self.is_corr_pose:
                if self.time_exer_state > 0:
                    # Decrease each second exercise state duration
                    if self.timer_exer_state.ticker(): self.time_exer_state -= 1
                else:
                    self.tng.exercise.set_next_state()
            # Handle when user done all exercise states
            self.done_exer_states = self.tng.exercise.state is None
            if not self.tng.exercise.state:
                self.tng.exercise.reps -=1
                if self.tng.exercise.reps > 0:
                    self.done_exer_reps = False
                    self.tng.exercise.reset_state()
                # Handle when user done all exercise repetitions
                else:
                    self.done_exer_reps = True
                    self.tap_next()
            # Handle when user done training
            if not self.tng.exercise: self.done()
