import Constants as cons
import Extensions as extn
from View.View import View

class ViewMain(View):
    """
    Responsible for drawing main view
    """
    def __init__(self):
        super().__init__()
        self.width = cons.window_width
        self.height = cons.window_height
        # Layout yoga and workout buttons
        self.bttn_yoga = extn.layout_corner_bttn(label=cons.lbl_yoga)
        self.bttn_workout = extn.layout_corner_bttn(left=False, label=cons.lbl_workout)
        self.add_subview(self.bttn_yoga)
        self.add_subview(self.bttn_workout)
