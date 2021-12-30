import logging
import cv2
import Constants as cons
import Extensions as extn
from Controller.ControllerMain import ControllerMain
import Controller.Hands as hands
import Controller.Detector as detector
import Router as router

def main():
    detector.init()
    root = ControllerMain()
    router.root = root
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
            root.view.appear(frame)
            # Show modal view
            if root.modal: root.modal.view.appear(frame)

            # Handle if user tap on yoga or workout button
            # ctrl_main.main()

            extn.draw_fps(root.view.frame)

            # Show frame
            cv2.imshow(cons.name_app, root.view.frame)
            # Handle quit from the app when user tap on keyboard
            if extn.is_quit(): break

        else:
            logging.debug('Cant read frame from the camera -> cap.read()')
            break

if __name__ == "__main__":
    main()