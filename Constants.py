import mediapipe as mp

# Names
name_app = 'AIgym'

# Formats
format_video = '.mp4'

# Files
f_poses = 'poses.json'

# Video
camera_id = 0
window_width = 960
window_height = 540
flip_hor = 1
flip_vert = 0
flip_both = -1

# Colors
clr_black = (0, 0, 0)
clr_white = (255, 255, 255)
clr_red = (0, 0, 255)
clr_green = (0, 255, 0)
clr_blue = (255, 0, 0)
clr_gray = (192,192,192)

# Training
duration_trng = 5 * 60 # mins, secs

# Indexes of all landmarks
NOSE = mp.solutions.pose.PoseLandmark.NOSE.value
LEFT_EYE_INNER = mp.solutions.pose.PoseLandmark.LEFT_EYE_INNER.value
LEFT_EYE = mp.solutions.pose.PoseLandmark.LEFT_EYE.value
LEFT_EYE_OUTER = mp.solutions.pose.PoseLandmark.LEFT_EYE_OUTER.value
RIGHT_EYE_INNER = mp.solutions.pose.PoseLandmark.RIGHT_EYE_INNER.value
RIGHT_EYE = mp.solutions.pose.PoseLandmark.RIGHT_EYE.value
RIGHT_EYE_OUTER = mp.solutions.pose.PoseLandmark.RIGHT_EYE_OUTER.value
LEFT_EAR = mp.solutions.pose.PoseLandmark.LEFT_EAR.value
RIGHT_EAR = mp.solutions.pose.PoseLandmark.RIGHT_EAR.value
MOUTH_LEFT = mp.solutions.pose.PoseLandmark.MOUTH_LEFT.value
MOUTH_RIGHT = mp.solutions.pose.PoseLandmark.MOUTH_RIGHT.value
LEFT_SHOULDER = mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value
RIGHT_SHOULDER = mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value
LEFT_ELBOW = mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value
RIGHT_ELBOW = mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value
LEFT_WRIST = mp.solutions.pose.PoseLandmark.LEFT_WRIST.value
RIGHT_WRIST = mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value
LEFT_PINKY = mp.solutions.pose.PoseLandmark.LEFT_PINKY.value
RIGHT_PINKY = mp.solutions.pose.PoseLandmark.RIGHT_PINKY.value
LEFT_INDEX = mp.solutions.pose.PoseLandmark.LEFT_INDEX.value
RIGHT_INDEX = mp.solutions.pose.PoseLandmark.RIGHT_INDEX.value
LEFT_THUMB = mp.solutions.pose.PoseLandmark.LEFT_THUMB.value
RIGHT_THUMB = mp.solutions.pose.PoseLandmark.RIGHT_THUMB.value
LEFT_HIP = mp.solutions.pose.PoseLandmark.LEFT_HIP.value
RIGHT_HIP = mp.solutions.pose.PoseLandmark.RIGHT_HIP.value
LEFT_KNEE = mp.solutions.pose.PoseLandmark.LEFT_KNEE.value
RIGHT_KNEE = mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value
LEFT_ANKLE = mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value
RIGHT_ANKLE = mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value
LEFT_HEEL = mp.solutions.pose.PoseLandmark.LEFT_HEEL.value
RIGHT_HEEL = mp.solutions.pose.PoseLandmark.RIGHT_HEEL.value
LEFT_FOOT_INDEX = mp.solutions.pose.PoseLandmark.LEFT_FOOT_INDEX.value
RIGHT_FOOT_INDEX = mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX.value

# Indexes of landmarks for pose classification and correction
lmks_main = [LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_ELBOW, RIGHT_ELBOW,
            LEFT_WRIST, RIGHT_WRIST, LEFT_HIP, RIGHT_HIP, LEFT_KNEE,
            RIGHT_KNEE, LEFT_ANKLE, RIGHT_ANKLE]

# Labels
lbl_pose = ' Pose'
lbl_done = 'Done!'
lbl_time_end = 'Time is end!'
lbl_pause = 'Pause'
lbl_next = 'Next'
lbl_exit = 'Exit'
lbl_continue = 'Continue'
lbl_yoga = 'Yoga'
lbl_workout = 'Workout'
lbl_correct_limbs = 'Correct red limbs'

# Font Sizes
fnt_size_timer = 2
fnt_size_menu = 1
fnt_thick = 2

# Time
time_wait_close_window = 10 # milliseconds
time_tap = 1 # seconds

# Keyboard
kbrd_quit = 'q'

# Global
num_big = 1000000000000

# View
view_circle_rad = 10
view_circle_filled_rad = 5

# Agnles
ang_pose_detect_gap = 20.0