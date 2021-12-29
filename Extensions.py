import cv2
import time as time
import Constants as cons
import os

dirname = os.path.dirname(__file__)

# Draw framerate
fps_prev_time = 0
def draw_fps(img):
    global fps_prev_time
    curr_time = time.time()
    fps = 1 / (curr_time - fps_prev_time)
    fps_prev_time = curr_time
    cv2.putText(img, str(int(fps)), (50, 500), cv2.FONT_HERSHEY_DUPLEX, cons.fnt_scale_menu, cons.clr_blue, cons.fnt_thick)

# Preprocess frame
def preprocess(frame):
    # Flip the frame horizontally for selfie-view
    frame = cv2.flip(frame, cons.flip_hor)
    return frame

def setup_video(name=cons.camera_id):
    video_name = os.path.join(dirname, name + cons.format_video) if name != cons.camera_id else name
    cap = cv2.VideoCapture(video_name)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cons.window_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cons.window_height)
    return cap

# Return if user tap on quit keyboard key
def is_quit():
    return cv2.waitKey(cons.time_wait_close_window) & 0xFF == ord(cons.kbrd_quit)