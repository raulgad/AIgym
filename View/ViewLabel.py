import Constants as cons
import cv2

class ViewLabel:
    """
    Responsible for label drawing
    """
    def __init__(self,
                x=0, y=0,
                text="",
                font=cv2.FONT_HERSHEY_DUPLEX,
                scale=cons.fnt_scale_menu,
                color=cons.clr_white,
                thick=cons.fnt_thick,
                ):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.scale = scale
        self.color = color
        self.thick = thick
        self.size = cv2.getTextSize(self.text, self.font, self.scale, self.thick)
        self.width = self.size[0][0]
        self.height = self.size[0][1]

    def draw(self, frame):
        pass