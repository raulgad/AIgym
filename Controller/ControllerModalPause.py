from View.ViewModalPause import ViewModalPause
from Controller.Controller import Controller

import Router as router

class ControllerModalPause(Controller):
    """
    Responsible for the logic of paused modal view controller
    """
    def __init__(self, super_ctrl):
        super().__init__()
        self.super_ctrl=super_ctrl
        # Layout paused modal view
        self.view = ViewModalPause()
        # Set callbacks to paused modal view buttons actions
        self.view.bttn_exit.action = self.tap_exit
        self.view.bttn_continue.action = self.tap_continue

    def tap_exit(self):
        # Import controller there for not get error 'cyclic imports'
        from Controller.ControllerMain import ControllerMain
        router.segue(fr=self, to=ControllerMain())
        
    def tap_continue(self):
        # Unpause train controller only if training time is not end
        self.super_ctrl.paused = self.super_ctrl.time_left_trng < 1
        # Unpause background video only if training time is not end
        self.super_ctrl.view.pause_background(self.super_ctrl.time_left_trng < 1)
        router.segue(fr=self)
        