import logging
import cv2
import Constants as cons
import Extensions as extn
from Controller.ControllerMain import ControllerMain
# from Controller.ControllerHands import ControllerHands
import Controller.ControllerHands as ctrl_hands
from Router import Router as router

def main():
    # Setup hands remote controller
    # ctrl_hands = ControllerHands()
    # Setup main controller
    ctrl_main = ControllerMain()
    # Get frame from the camera
    while ctrl_main.view.cap.isOpened():
        success, frame = ctrl_main.view.cap.read()
        if success:
            # Preprocess frame
            ctrl_main.view.preprocess(frame)
            # Detect pose landmarks and segmentation mask
            
            ctrl_main.analyze_user()
            ctrl_hands.set(ctrl_main.lmks)

            # Show main view
            router.segue(ctrl_main.view)

            # Handle if user tap on yoga or workout button
            # ctrl_main.main()

            extn.draw_fps(ctrl_main.view.frame)

            # Show frame
            cv2.imshow(cons.name_app, ctrl_main.view.frame)
            # Handle quit from the app when user tap on keyboard
            if ctrl_main.is_quit(): break

        else:
            logging.debug('Cant read frame from the camera -> cap.read()')
            break

if __name__ == "__main__":
    main()