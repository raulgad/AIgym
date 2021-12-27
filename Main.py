import cv2
import os
import time
import Constants as cons
import Extensions as extn
from View.ViewMain import ViewMain
from Controller.ControllerMain import ControllerMain
from Controller.ControllerHands import ControllerHands

def main():
    # Setup main view of the app
    # vw_main = ViewMain()

    # Setup main controller
    ctrl_main = ControllerMain(view = ViewMain())
    # Setup hands remote controller
    ctrl_hands = ControllerHands()

    # Get frame from the camera
    while ctrl_main.view.cap.isOpened():
        success, frame = ctrl_main.view.cap.read()
        if success:
            # Preprocess frame
            ctrl_main.view.preprocess(frame)

            # Set pose landmarks and segmentation mask
            ctrl_main.analyze()
            ctrl_hands.set(ctrl_main.lmks)

            ctrl_main.view.appear()

            extn.draw_fps(ctrl_main.view.frame)

            # Show frame
            cv2.imshow(cons.name_app, ctrl_main.view.frame)
            # Handle quit from the app when user tap on keyboard
            if ctrl_main.is_quit(): break

        else:
            print('Cant read frame from the camera -> cap.read()')
            break

if __name__ == "__main__":
    main()