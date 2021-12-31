from View.ViewMain import ViewMain
from Controller.Controller import Controller
from Controller.ControllerTrain import ControllerTrain
import Router as router

class ControllerMain(Controller):
    """
    Responsible for the main logic
    """
    def __init__(self):
        super().__init__()
        # Layout main view
        self.view = ViewMain()
        # Set callbacks to main buttons actions
        self.view.bttn_yoga.action = self.tap_yoga
        self.view.bttn_workout.action = self.tap_workout

    def tap_yoga(self):
        print("tap_yoga")
        router.segue(fr=self, to=ControllerTrain())

    def tap_workout(self):
        print("tap_workout")


