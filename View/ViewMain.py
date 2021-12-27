import Constants as cons
import cv2

from View.ViewButton import ViewButton
from View.ViewLabel import ViewLabel

class ViewMain:
    """
    Responsible for drawing main view
    """
    def __init__(self):
        self.draw = True
        self.frame = []
        self.window_width = cons.window_width
        self.window_height = cons.window_height
        # Setup video from camera
        self.cap = cv2.VideoCapture(cons.camera_id)
        self.set_window_size(self.cap)
        cv2.namedWindow(cons.name_app, cv2.WINDOW_NORMAL)
        # Setup buttons
        yoga_bttn_x_end = cons.vw_bttn_spacing + int(cons.vw_bttn_width * self.window_width)
        yoga_bttn_y_end = cons.vw_bttn_spacing + int(cons.vw_bttn_height * self.window_height)
        yoga_bttn_label = ViewLabel(x=cons.vw_bttn_spacing + int(yoga_bttn_x_end / 3.2), 
                                    y=cons.vw_bttn_spacing + int(yoga_bttn_y_end / 1.7),
                                    text=cons.lbl_yoga)
        self.yoga_bttn = ViewButton(x=cons.vw_bttn_spacing, y=cons.vw_bttn_spacing,
                                    x_end=yoga_bttn_x_end, y_end=yoga_bttn_y_end,
                                    label=yoga_bttn_label)

        
        # self.point_radius_inner = cons.vw_train_circle_filled_rad
        # self.point_radius = cons.vw_train_circle_rad
        
        # # Setup background video 
        # bg_video_name = os.path.join(os.path.dirname(__file__), 'pose_1' + cons.format_video)
        # self.cap_backgrd = cv2.VideoCapture(bg_video_name)
        # self.set_window_size(self.cap_backgrd)
    
    def preprocess(self, img):
        # Flip the frame horizontally for selfie-view
        self.frame = cv2.flip(img, cons.flip_hor)
        return self.frame

    def set_window_size(self, cap):
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.window_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.window_height) 

    def appear(self):
        if self.draw:
            # Draw buttons
            self.yoga_bttn.draw(self.frame)
            
    def disappear():
        pass



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