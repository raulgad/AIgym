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
        self.cap_backgrd = None
        self.paused = False
        self.tng = None
        self.tng_active = True
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

    def tap_pause(self):
        self.paused = True
        self.view.pause_background()
        router.segue(fr=self, to=ControllerModalPause(super_ctrl=self), modal=True)

    def tap_next(self):
        if self.tng_active:
            # Set next background video
            self.cap_backgrd = extn.setup_video(cons.dir_yoga, 'warrior')

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
                self.view.bttn_pause.filled_width = self.view.bttn_pause.width
                self.view.pose_label.text = cons.lbl_time_end
                self.view.bttn_pause.label.text = cons.lbl_pause
                self.tng_active = False
                self.view.pause_background()
            
            incorr_angs = self.tng.incorr_angs(self.tng.exercise.state.angles)
            is_corr_pose = not incorr_angs
            self.view.draw_corrections(incorr_angs)

    # def tng_timing(self):
    #     # Handle training timing
    #     if self.time_left_tng > 0:
    #         # Check if one second has passed
    #         if self.timer_tng.ticker():
    #             # Update pause button view
    #             self.time_left_tng -= 1
    #             trng_mins, trng_secs = divmod(self.time_left_tng, 60)
    #             self.view.bttn_pause.label.text = cons.lbl_pause + ' {:02d}:{:02d}'.format(trng_mins, trng_secs)
    #             self.view.fill_background(self.view.bttn_pause, self.bttn_pause_fill_step)
    #     # Handle when training time is end
    #     else:
    #         self.view.bttn_pause.filled_width = self.view.bttn_pause.width
    #         self.view.pose_label.text = cons.lbl_time_end
    #         self.view.bttn_pause.label.text = cons.lbl_pause
    #         self.tng_active = False
    #         self.view.pause_background()