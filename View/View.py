class View:
    """
    Responsible for drawing in all views
    """
    def __init__(self):
        self.super = None
        self.is_draw = True
        self.frame = []
        self.subviews = []

    def add_subview(self, subview):
        subview.super = self
        self.subviews.append(subview)

    def appear(self, frame):
        if self.is_draw:
            self.frame = frame
            self.draw()
            # Draw subviews
            if self.subviews:
                for subview in self.subviews: subview.appear(self.frame)

    def disappear(self):
        self.is_draw = False
    
    def draw(self):
        pass