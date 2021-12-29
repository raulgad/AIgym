import logging
import cv2
import Constants as cons
import Extensions as extn
from Controller.ControllerMain import ControllerMain
import Controller.ControllerHands as hands
import Controller.ControllerDetector as detector
# import Router as router

def main():
    detector.init()
    # Setup main controller
    ctrl_main = ControllerMain()
    # Setup video from the camera
    cap = extn.setup_video()
    # Get frame from the camera
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            # Preprocess frame
            frame = extn.preprocess(frame)
            # Detect pose landmarks and segmentation mask
            detector.analyze_user(frame)
            # Set hands coordinates for remote controll
            hands.set()

            # Show main view
            ctrl_main.view.frame = frame
            ctrl_main.view.appear()

            # router.segue(ctrl_main.view)

            # Handle if user tap on yoga or workout button
            # ctrl_main.main()

            extn.draw_fps(ctrl_main.view.frame)

            # Show frame
            cv2.imshow(cons.name_app, ctrl_main.view.frame)
            # Handle quit from the app when user tap on keyboard
            if extn.is_quit(): break

        else:
            logging.debug('Cant read frame from the camera -> cap.read()')
            break

if __name__ == "__main__":
    main()