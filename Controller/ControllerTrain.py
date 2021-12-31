from View.ViewTrain import ViewTrain
from Controller.Controller import Controller
from Controller.ControllerModalPause import ControllerModalPause
import Router as router

class ControllerTrain(Controller):
    """
    Responsible for the train logic
    """
    def __init__(self):
        super().__init__()
        # Layout train view
        self.view = ViewTrain()
        # Set callbacks to train buttons actions
        self.view.bttn_pause.action = self.tap_pause
        self.view.bttn_next.action = self.tap_next

    def tap_pause(self):
        print("tap_pause")
        router.segue(fr=self, to=ControllerModalPause(), modal=True)

    def tap_next(self):
        print("tap_next")
        