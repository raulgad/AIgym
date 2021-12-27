import Constants as cons
import cv2

class ViewLabel:
    """
    Responsible for label drawing
    """
    def __init__(self,
                x, y,
                text="",
                font=cv2.FONT_HERSHEY_DUPLEX,
                size=cons.fnt_size_menu,
                color=cons.clr_white,
                thick=cons.fnt_thick,
                ):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.size = size
        self.color = color
        self.thick = thick

    def draw(self, frame):
        pass