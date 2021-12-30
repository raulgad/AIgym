import Constants as cons
from View.ViewButton import ViewButton
from View.ViewLabel import ViewLabel
from View.View import View

class ViewMain(View):
    """
    Responsible for drawing main view
    """
    def __init__(self):
        super().__init__()
        self.width = cons.window_width
        self.height = cons.window_height
        # Setup yoga button
        bttn_width = int(cons.vw_bttn_width * self.width)
        bttn_height = int(cons.vw_bttn_height * self.height)
        self.bttn_yoga = ViewButton(x=cons.vw_bttn_spacing, y=cons.vw_bttn_spacing,
                                    x_end=cons.vw_bttn_spacing + bttn_width, 
                                    y_end=cons.vw_bttn_spacing + bttn_height,
                                    label=ViewLabel(text=cons.lbl_yoga),
                                    center_label=True)
        # Setup workout button
        self.bttn_workout = ViewButton(x=self.width - (cons.vw_bttn_spacing + bttn_width), 
                                    y=cons.vw_bttn_spacing,
                                    x_end=self.width - cons.vw_bttn_spacing, 
                                    y_end=cons.vw_bttn_spacing + bttn_height,
                                    label=ViewLabel(text=cons.lbl_workout),
                                    center_label=True)
        self.add_subview(self.bttn_yoga)
        self.add_subview(self.bttn_workout)


    # self.point_radius_inner = cons.vw_train_circle_filled_rad
    # self.point_radius = cons.vw_train_circle_rad
    
    # # Setup background video 
    # bg_video_name = os.path.join(os.path.dirname(__file__), 'pose_1' + cons.format_video)
    # self.cap_backgrd = cv2.VideoCapture(bg_video_name)
    # self.set_window_size()


# def draw_point(self, img, x, y, clr=cons.clr_red):
#     cv2.circle(img, (x, y), self.point_radius_inner, clr, cv2.FILLED)
#     cv2.circle(img, (x, y), self.point_radius, clr)

# def draw_line(self, img, lmks, points=[], clr=cons.clr_white, point_clr=cons.clr_white):
#     for p_idx, point in enumerate(points):
#         # Draw first point
#         x1, y1, _ = lmks[point]
#         self.draw_point(img, x1, y1, clr=point_clr)
#         # Draw line to next point
#         if p_idx + 1 < len(points):
#             x2, y2, _ = lmks[points[p_idx + 1]]
#             cv2.line(img, (x1, y1), (x2, y2), clr, cons.fnt_thick)
#             self.draw_point(img, x2, y2, clr=point_clr)