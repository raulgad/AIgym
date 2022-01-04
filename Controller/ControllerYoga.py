import Constants as cons
import Extensions as extn
from Controller.ControllerTrain import ControllerTrain
from View.ViewYoga import ViewYoga

class ControllerYoga(ControllerTrain):
    """
    Responsible for the yoga logic
    """
    def __init__(self):
        super().__init__()
        # Set background video with coach
        self.cap_backgrd = extn.setup_video(cons.dir_yoga, 't')
        # Set youga training duration
        self.duration_trng = 7 * 60 # mins, secs
        self.trng_time_left = self.duration_trng
        
        self.bttn_pause_fill_step = self.view.bttn_pause.width / self.duration_trng
        self.view.bttn_pause.filled_less_one = self.bttn_pause_fill_step


    def run(self):
        if self.trng_time_left > 0:
            # Check if one second has passed
            if extn.timeticker():
                # Update pause button view
                self.trng_time_left -= 1
                trng_mins, trng_secs = divmod(self.trng_time_left, 60)
                self.view.bttn_pause.label.text = cons.lbl_pause + ' {:02d}:{:02d}'.format(trng_mins, trng_secs)
                self.view.fill_background(self.view.bttn_pause, self.bttn_pause_fill_step)
        # Handle training time is end
        else:
            self.view.bttn_pause.filled_width = self.view.bttn_pause.width
            self.view.pose_label.text = cons.lbl_time_end
            self.view.bttn_pause.label.text = cons.lbl_pause
            self.view.pause_background()
