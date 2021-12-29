import logging
import mediapipe as mp
import cv2
import Constants as cons
from View.ViewMain import ViewMain

class ControllerMain:
    """
    Responsible for the main logic
    """
    def __init__(self):
        self.view = ViewMain()

    # def main(self):
    #     if self.ctrl_hands.tapped(self.view.bttn_yoga):
    #         pass
    #     elif self.ctrl_hands.tapped(self.view.bttn_workout):
    #         pass
    
    def is_quit(self):
        # Return if user tap on quit keyboard key
        return cv2.waitKey(cons.time_wait_close_window) & 0xFF == ord(cons.kbrd_quit)
