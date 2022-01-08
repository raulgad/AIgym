import Constants as cons
from View.View import View
from View.ViewButton import ViewButton
from View.ViewLabel import ViewLabel

class ViewModalPause(View):
    """
    Responsible for drawing paused modal view
    """
    def __init__(self):
        super().__init__()
        self.width = cons.window_width
        self.height = cons.window_height
        # Layout exit button
        spacing_between_bttns = cons.vw_bttn_spacing * 6
        # Horizontally centerize buttons
        x_exit = int(cons.window_width / 2 - (cons.vw_bttn_width + spacing_between_bttns / 2))
        y_exit = int(cons.window_height * 0.4)
        x_exit_end = x_exit + cons.vw_bttn_width
        y_exit_end = y_exit + cons.vw_bttn_height
        self.bttn_exit = ViewButton(x=x_exit, y=y_exit, x_end=x_exit_end, y_end=y_exit_end, 
                    label=ViewLabel(text=cons.lbl_exit), center_label=True)
        # Layout continue button
        x_continue = x_exit_end + spacing_between_bttns
        self.bttn_continue = ViewButton(x=x_continue, y=y_exit, x_end= x_continue + cons.vw_bttn_width, y_end= y_exit_end, 
                    label=ViewLabel(text=cons.lbl_continue), center_label=True)
        self.add_subview(self.bttn_exit)
        self.add_subview(self.bttn_continue)
        