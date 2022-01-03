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
    router.root = ControllerMain()
    # Setup video from the camera
    cap = extn.setup_video()
    cv2.namedWindow(cons.name_app, cv2.WINDOW_NORMAL)
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
            router.root.view.appear(frame)
            # Show modal view
            if router.root.modal: router.root.modal.view.appear(router.root.view.frame)
            # Render frame
            try:
                
                extn.draw_fps(router.root.view.frame)

                cv2.imshow(cons.name_app, router.root.view.frame)
            except:
                logging.debug('Cant render the frame -> cv2.imshow()')
            # Quit from the app when user tap on keyboard
            if extn.is_quit(): break

        else:
            logging.debug('Cant read frame from the camera -> cap.read()')
            break

if __name__ == "__main__":
    main()