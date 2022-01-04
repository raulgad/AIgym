import numpy as np
import cv2
import Constants as cons
import Extensions as extn
import Controller.Detector as detector
from View.View import View
from View.ViewLabel import ViewLabel

class ViewTrain(View):
    """
    Responsible for drawing train view
    """
    def __init__(self, ctrl):
        super().__init__()
        self.width = cons.window_width
        self.height = cons.window_height
        self.ctrl = ctrl
        self.backgrd_frame = None
        self.paused_backgrd_frame = None
        self.paused_frame_idx = None
        # Layout pause and next buttons
        self.bttn_pause = extn.layout_corner_bttn(label=cons.lbl_pause, center_label=False, backgr_clr=cons.clr_gray)
        self.bttn_next = extn.layout_corner_bttn(left=False, label=cons.lbl_next, backgr_clr=cons.clr_gray)
        self.add_subview(self.bttn_pause)
        self.add_subview(self.bttn_next)
        # Layout pose label
        self.pose_label = ViewLabel(color=cons.clr_red, text=cons.lbl_correct_limbs)
        self.pose_label.y = self.bttn_pause.label.y
        # Horizontally centerize pose label
        self.pose_label.x = int(self.width / 2 - self.pose_label.width / 2)
        self.add_subview(self.pose_label)

    def appear(self, frame):
        if self.is_draw:
            self.frame = frame
            # Read background video frame
            if self.ctrl.cap_backgrd and detector.segmentation_mask is not None:
                success, self.backgrd_frame = self.ctrl.cap_backgrd.read()
                # Set paused background frame if we in paused state
                if self.paused_backgrd_frame is not None: 
                    self.backgrd_frame = self.paused_backgrd_frame
                # Repeat video if it's end
                if not success:
                    self.ctrl.cap_backgrd.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    _, self.backgrd_frame = self.ctrl.cap_backgrd.read()
                # Add background frame to segmented user's frame
                self.add_background()
                # Show frame with background video under the train's subviews
                super().appear(self.frame)
            # Give runtime to the parent controller
            self.ctrl.run()

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

    def add_background(self):
        # Add background frame to segmented user's frame
        condition = np.stack((detector.segmentation_mask,) * 3, axis=-1) > 0.1
        self.frame = np.where(condition, self.frame, np.array(self.backgrd_frame).astype(np.uint8))

    def pause_background(self, pause=True):
        if pause:
            # Save paused frame
            self.paused_backgrd_frame = self.backgrd_frame
            self.paused_frame_idx = self.ctrl.cap_backgrd.get(cv2.CAP_PROP_POS_FRAMES)
        else:
            self.paused_backgrd_frame = None
            # Start video from paused state
            self.ctrl.cap_backgrd.set(cv2.CAP_PROP_POS_FRAMES, self.paused_frame_idx)

    def fill_background(self, button, step):
        # Fill button's background only if accumulated steps are more than 1 otherwise wait \
        # we need it to handle cases when step is less than one pixel
        
        # print(button, step)
        if button.filled_less_one < 1:
            button.filled_less_one += step
        else:
            button.filled_less_one = step
            button.filled_width += 1
        if step >= 1:
            button.filled_width += int(step)
