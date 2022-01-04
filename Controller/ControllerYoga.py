import Constants as cons
import Extensions as extn
from Controller.ControllerTrain import ControllerTrain
from Timing import Timing

class ControllerYoga(ControllerTrain):
    """
    Responsible for yoga logic
    """
    def __init__(self):
        super().__init__()
        # Set background video with coach
        self.cap_backgrd = extn.setup_video(cons.dir_yoga, 't')
        # Set durations
        duration_trng = 7 * 60 # mins, secs
        self.time_left_trng = duration_trng
        duration_pose = 10
        self.time_left_pose = duration_pose
        # Setup button's background filled parts
        self.bttn_pause_fill_step = self.view.bttn_pause.width / duration_trng
        self.view.bttn_pause.filled_less_one = self.bttn_pause_fill_step
        self.bttn_next_fill_step = self.view.bttn_next.width / duration_pose
        self.view.bttn_next.filled_less_one = self.bttn_next_fill_step
        # Set timers
        self.trng_timer = Timing()
        self.pose_timer = Timing()

    def run(self):
        if not self.paused:
            # Handle training views updating
            if self.time_left_trng > 0:
                # Check if one second has passed
                if self.trng_timer.ticker():
                    # Update pause button view
                    self.time_left_trng -= 1
                    trng_mins, trng_secs = divmod(self.time_left_trng, 60)
                    self.view.bttn_pause.label.text = cons.lbl_pause + ' {:02d}:{:02d}'.format(trng_mins, trng_secs)
                    self.view.fill_background(self.view.bttn_pause, self.bttn_pause_fill_step)
            # Handle training time is end
            else:
                self.view.bttn_pause.filled_width = self.view.bttn_pause.width
                self.view.pose_label.text = cons.lbl_time_end
                self.view.bttn_pause.label.text = cons.lbl_pause
                self.view.pause_background()
            
            # Handle pose views updating
            if self.time_left_pose > 0:
                # Check if one second has passed
                if self.pose_timer.ticker():
                    self.time_left_pose -= 1
                    self.view.fill_background(self.view.bttn_next, self.bttn_next_fill_step)
            # Handle pose time is end
            else:
                self.view.bttn_next.filled_width = self.view.bttn_next.width
                