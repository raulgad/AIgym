import logging
import mediapipe as mp
import cv2
import Constants as cons
from View.ViewMain import ViewMain

class ControllerMain:
    """
    Responsible for the main logic
    """
    def __init__(self, static_image_mode=False, model_complexity=0, smooth_landmarks=True, 
                enable_segmentation=True, smooth_segmentation=True,
                min_detection_confidence=0.5, min_tracking_confidence=0.5):
        
        self.mpipepose = self.mpipepose = mp.solutions.pose.Pose(static_image_mode, model_complexity, 
                                    smooth_landmarks, enable_segmentation, 
                                    smooth_segmentation, min_detection_confidence, 
                                    min_tracking_confidence)
        self.view = ViewMain()

    def analyze_user(self):
        # Detect pose landmarks and segmentation mask from the frame
        imgRGB = cv2.cvtColor(self.view.frame, cv2.COLOR_BGR2RGB)
        results = self.mpipepose.process(imgRGB)
        self.lmks = []
        self.segmentation_mask = results.segmentation_mask
        try:
            if results.pose_landmarks:
                # Get coordinates of the landmarks according to the screen size
                for lm in results.pose_landmarks.landmark:
                    height, width, _ = self.view.frame.shape
                    cx, cy, cz = int(lm.x * width), int(lm.y * height), int(lm.z * width)
                    self.lmks.append([cx, cy, cz])
        except:
            logging.debug('Something goes wrong in analyze() -> ControllerMain')
            pass

    # def main(self):
    #     if self.ctrl_hands.tapped(self.view.bttn_yoga):
    #         pass
    #     elif self.ctrl_hands.tapped(self.view.bttn_workout):
    #         pass
    
    def is_quit(self):
        # Return if user tap on quit keyboard key
        return cv2.waitKey(cons.time_wait_close_window) & 0xFF == ord(cons.kbrd_quit)
