import cv2
import Constants as cons
import View.ViewLabel as ViewLabel
import Controller.Hands as hands
from View.View import View
import Router as router

class ViewButton(View):
    """
    Responsible for button drawing
    """
    # Class variable for activate only one button at time
    has_focused = False

    def __init__(self, 
                x, y,
                x_end, y_end,
                filled_divider=1, 
                frame_thick=cons.vw_bttn_frame_thick, 
                frame_clr=cons.clr_black, 
                backgr_clr=cons.clr_black,
                label=ViewLabel,
                action=None,
                center_label=False,
                ) -> None:
        super().__init__()
        self.is_active = True
        self.x = x
        self.y = y
        self.x_end = x_end
        self.y_end = y_end
        self.width = self.x_end - self.x
        self.height = self.y_end - self.y
        self.fill_step = self.width / filled_divider
        self.frame_clr = frame_clr
        self.frame_thick = frame_thick
        self.backgr_clr = backgr_clr
        self.label = label
        self.action = action
        # Centerize label if needed
        if center_label:
            self.label.x = int(self.x + self.width / 2 - self.label.width / 2)
            self.label.y = int(self.y + self.height / 2 + self.label.height / 2)

    def appear(self, frame):
        if self.is_draw:
            # Deactivate button (not highlighted and tappable) if it isnt on the main screen
            if not router.shown(self): self.is_active = False
            super().appear(frame)

        # if self.action:
        #     self.action()
            
    def draw(self):
        # Highlight button if hand in its area
        focused = hands.focus(self)
        frame_highlight_color = cons.clr_green if focused and self.is_active and not ViewButton.has_focused else self.frame_clr
        ViewButton.has_focused = focused
        # Draw button frame
        cv2.rectangle(self.frame,
                        (self.x, self.y), 
                        (self.x_end, self.y_end), 
                        frame_highlight_color, 
                        self.frame_thick)
        # Draw button background. 
        # Button is filled if its frame color is equal the background color.
        filled_clr = self.frame_clr if self.backgr_clr == self.frame_clr else self.backgr_clr
        cv2.rectangle(self.frame, 
                        (self.x, self.y), 
                        (self.x_end, self.y_end), 
                        filled_clr, 
                        cv2.FILLED)
        # Draw button's partially filled part
        if self.fill_step > 0 and self.fill_step < self.width:
            cv2.rectangle(self.frame, 
                            (self.x, self.y), 
                            (self.x_end + self.fill_step, self.y_end), 
                            self.frame_clr, 
                            cv2.FILLED)
        # Draw button label
        if self.label:
            cv2.putText(self.frame, 
                        self.label.text, 
                        (self.label.x, self.label.y), 
                        self.label.font, 
                        self.label.scale, 
                        self.label.color, 
                        self.label.thick)
