from View.ViewMain import ViewMain
from Controller.Controller import Controller

class ControllerMain(Controller):
    """
    Responsible for the main logic
    """
    def __init__(self):
        super().__init__()
        self.view = ViewMain()
        self.view.bttn_yoga.action = self.tap_yoga
        self.view.bttn_workout.action = self.tap_workout

    def tap_yoga(self):
        print("tap_yoga")

    def tap_workout(self):
        print("tap_workout")


