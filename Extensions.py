import cv2
import time as time
import Constants as cons

# Draw framerate
fps_prev_time = 0

def draw_fps(img):
    global fps_prev_time
    curr_time = time.time()
    fps = 1 / (curr_time - fps_prev_time)
    fps_prev_time = curr_time
    cv2.putText(img, str(int(fps)), (50, 500), cv2.FONT_HERSHEY_DUPLEX, cons.fnt_size_menu, cons.clr_blue, cons.fnt_thick)