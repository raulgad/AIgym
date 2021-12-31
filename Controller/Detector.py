import logging
import cv2
import mediapipe as mp

"""
Responsible for detecting
"""

mpipepose = None
lmks = [-1] * len(mp.solutions.pose.PoseLandmark)
segmentation_mask = []

def init(static_image_mode=False, model_complexity=0, smooth_landmarks=True, 
                enable_segmentation=True, smooth_segmentation=True,
                min_detection_confidence=0.5, min_tracking_confidence=0.5):
    global mpipepose
    mpipepose = mp.solutions.pose.Pose(static_image_mode, model_complexity, 
                                    smooth_landmarks, enable_segmentation, 
                                    smooth_segmentation, min_detection_confidence, 
                                    min_tracking_confidence)

def analyze_user(frame):
    global mpipepose
    global lmks
    global segmentation_mask
    # Detect pose landmarks and segmentation mask from the frame
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mpipepose.process(imgRGB)
    segmentation_mask = results.segmentation_mask
    try:
        if results.pose_landmarks:
            
            mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks,
                                           mp.solutions.pose.POSE_CONNECTIONS)

            # Get coordinates of the landmarks according to the screen size
            for idx, lm in enumerate(results.pose_landmarks.landmark):
                height, width, _ = frame.shape
                cx, cy, cz = int(lm.x * width), int(lm.y * height), int(lm.z * width)
                lmks[idx] = [cx, cy, cz]
    except:
        logging.debug('Something goes wrong in analyze() -> ControllerMain')
        pass
    