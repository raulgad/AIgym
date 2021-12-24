from os import X_OK
import Constants as cons

class ViewButton:
    """
    Responsible for button drawing
    """
    def __init__(self, 
                x, y, 
                width, height, 
                w_divider=1, 
                frame_clr=cons.clr_black, 
                frame_thick=cons.fnt_thick, 
                backgr_clr=cons.clr_black,
                labels=[]
                ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.width_step = width / w_divider
        self.height = height
        self.frame_clr = frame_clr
        self.frame_thick = frame_thick
        self.backgr_clr = backgr_clr
        self.labels = labels

