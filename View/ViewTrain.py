import os
import cv2
import Constants as cons
from View.ViewButton import ViewButton
from View.ViewLabel import ViewLabel
from View.View import View
import Controller.Detector as detector
import Extensions as extn

class ViewTrain(View):
    """
    Responsible for drawing train view
    """
    def __init__(self):
        super().__init__()
        self.width = cons.window_width
        self.height = cons.window_height
        # Setup background video 
        bg_video_name = os.path.join(os.path.dirname(__file__), 'pose_1' + cons.format_video)
        self.cap_backgrd = extn.setup_video(bg_video_name)
        # Layout pause and next buttons
        self.bttn_pause = extn.layout_corner_bttn(label=cons.lbl_pause, backgr_clr=cons.clr_gray)
        self.bttn_next = extn.layout_corner_bttn(left=False, label=cons.lbl_next, backgr_clr=cons.clr_gray)
        self.add_subview(self.bttn_pause)
        self.add_subview(self.bttn_next)

    def draw_point(self, x, y, clr=cons.clr_red):
        cv2.circle(self.frame, (x, y), cons.vw_train_circle_filled_rad, clr, cv2.FILLED)
        cv2.circle(self.frame, (x, y), cons.vw_train_circle_rad, clr)

    def draw_line(self, points=[], clr=cons.clr_white, point_clr=cons.clr_white):
        for p_idx, point in enumerate(points):
            # Draw first point
            x1, y1, _ = detector.lmks[point]
            self.draw_point(self.frame, x1, y1, clr=point_clr)
            # Draw line to next point
            if p_idx + 1 < len(points):
                x2, y2, _ = detector.lmks[points[p_idx + 1]]
                cv2.line(self.frame, (x1, y1), (x2, y2), clr, cons.fnt_thick)
                self.draw_point(self.frame, x2, y2, clr=point_clr)