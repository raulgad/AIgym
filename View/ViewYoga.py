from View.ViewTrain import ViewTrain

class ViewYoga(ViewTrain):
    """
    Responsible for drawing yoga view
    """
    def __init__(self, ctrl):
        super().__init__(ctrl)
    
    def appear(self, frame):
        if self.is_draw:
            super().appear(frame)

