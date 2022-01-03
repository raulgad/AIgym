import os
import logging
from View.ViewTrain import ViewTrain
from Controller.Controller import Controller
from Controller.ControllerModalPause import ControllerModalPause
import Router as router
import Constants as cons
import Extensions as extn

class ControllerTrain(Controller):
    """
    Responsible for the train logic
    """
    def __init__(self):
        super().__init__()
        self.cap_backgrd = None
        # Layout train view
        self.view = ViewTrain(ctrl=self)
        # Set callbacks to train buttons actions
        self.view.bttn_pause.action = self.tap_pause

        # self.view.bttn_next.action = self.tap_next
        self.cap_backgrd = extn.setup_video(cons.dir_yoga, 't')

    def tap_pause(self):
        logging.debug('tap_pause')
        self.view.pause_background()
        router.segue(fr=self, to=ControllerModalPause(super_ctrl=self), modal=True)

    # def tap_next(self):
    #     logging.debug('tap_next')
    #     self.set_backgrd_video(cons.dir_yoga, 't')

    # def set_backgrd_video(self, dir, name):
    #     self.cap_backgrd = extn.setup_video(dir, name)

        