from View.ViewMain import ViewMain
from Controller.Controller import Controller

class ControllerMain(Controller):
    """
    Responsible for the main logic
    """
    def __init__(self):
        super().__init__()
        self.view = ViewMain()

    # def main(self):
    #     if self.ctrl_hands.tapped(self.view.bttn_yoga):
    #         pass
    #     elif self.ctrl_hands.tapped(self.view.bttn_workout):
    #         pass
    

