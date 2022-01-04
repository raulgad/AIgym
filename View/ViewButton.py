import cv2
import time
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
    one_active = False

    def __init__(self, 
                x, y,
                x_end, y_end,
                frame_thick=cons.vw_bttn_frame_thick, 
                frame_clr=cons.clr_black, 
                backgr_clr=cons.clr_black,
                label=ViewLabel,
                action=None,
                center_label=False,
                ) -> None:
        super().__init__()
        self.is_active = True
        self.is_focused = False
        self.time_start_focus = 0
        self.is_tapped = False
        self.x = x
        self.y = y
        self.x_end = x_end
        self.y_end = y_end
        self.width = self.x_end - self.x
        self.height = self.y_end - self.y
        self.filled_width = 0
        self.filled_less_one = 0
        self.frame_clr = frame_clr
        self.frame_thick = frame_thick
        self.backgr_clr = backgr_clr
        self.label = label
        self.action = action
        # Centerize label.x if needed
        self.label.x = int(self.x + self.width / 2 - self.label.width / 2) if center_label else self.x + cons.vw_bttn_spacing
        self.label.y = int(self.y + self.height / 2 + self.label.height / 2)

    def appear(self, frame):
        if self.is_draw:
            # Deactivate button (not highlighted and tappable) if it isnt on the main screen, 
            # eg when modal view is shown
            self.is_active = router.shown(self)
            super().appear(frame)
            # Handle tap on the button
            if self.is_active and self.action and self.tapped(): self.action()
            # Set that the one of the buttons is now focused
            ViewButton.one_active = self.is_focused
            
    def draw(self):
        self.is_focused = hands.focus(self)
        # Highlight button if it focused
        frame_highlight_color = cons.clr_green if self.is_focused and self.is_active and not ViewButton.one_active else self.frame_clr
        # Draw button frame
        cv2.rectangle(self.frame,
                        (self.x, self.y), 
                        (self.x_end, self.y_end), 
                        frame_highlight_color, 
                        self.frame_thick)
        # Draw button background. 
        # Button is filled if its frame color is equal the background color
        filled_clr = self.frame_clr if self.backgr_clr == self.frame_clr else self.backgr_clr
        cv2.rectangle(self.frame, 
                        (self.x, self.y), 
                        (self.x_end, self.y_end), 
                        filled_clr, 
                        cv2.FILLED)
        # Draw button's partially filled part
        if self.filled_width > 0:
            cv2.rectangle(self.frame, 
                            (self.x, self.y), 
                            (self.x + self.filled_width, self.y_end), 
                            self.frame_clr, 
                            cv2.FILLED)
        # Full fill background if filled part goes beyond width
        elif self.filled_width >= self.width:
            self.filled_width = self.width
        # Draw button label
        if self.label:
            cv2.putText(self.frame, 
                        self.label.text, 
                        (self.label.x, self.label.y), 
                        self.label.font, 
                        self.label.scale, 
                        self.label.color, 
                        self.label.thick)
    
    def tapped(self):
        # Detect tap if button in focus and we dont have any other focused button
        if self.is_focused and not ViewButton.one_active:
            # Reinit 'time_start_focus' when user start focus the button
            if not self.time_start_focus:
                self.time_start_focus = time.time()
            # Check if user's hand is focused certain time on the button 
            time_in_focus = int(time.time() - self.time_start_focus)
            if time_in_focus == cons.time_tap and not self.is_tapped:
                self.time_start_focus = 0
                self.is_tapped = True
                return True
        else:
            self.time_start_focus = 0
            self.is_tapped = False
