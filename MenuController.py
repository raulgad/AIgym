import Constants as cons

class MenuController:
    """
    Responsible for the logic of the menu buttons
    """

    def __init__(self) -> None:
        self.pause_bttn_active = True
        self.next_bttn_active = True
        self.exit_butt_active = False
        self.cont_butt_active = False
        self.yoga_butt_active = True
        self.workout_butt_active = True

        # self.lhand_in_pause_bttn = False
        # self.rhand_in_pause_bttn = False
        # self.lhand_in_next_bttn = False
        # self.rhand_in_next_bttn = False
        # self.lhand_in_exit_butt = False
        # self.rhand_in_exit_butt = False
        # self.lhand_in_cont_butt = False
        # self.rhand_in_cont_butt = False
        # self.lhand_in_yoga_butt = False
        # self.rhand_in_yoga_butt = False
        # self.lhand_in_workout_butt = False
        # self.rhand_in_workout_butt = False

        self.next_bttn_tapped = False
        self.pause_bttn_tapped = False
        self.exit_butt_tapped = False
        self.cont_butt_tapped = False
        self.yoga_butt_tapped = False
        self.workout_butt_tapped = False

        self.some_bttn_active = False
        
    def set_hands_coords(self, lmks):
        # Set current coordinates of left (l) and right (r) hands
        self.l_x, self.l_y, _ = lmks[cons.RIGHT_INDEX]
        self.r_x, self.r_y, _ = lmks[cons.LEFT_INDEX]

    def hand_focus(self, bttn) -> bool:
        # Return if user hand in button area and not some other button is active
        # Check if left hand in the area
        l_x_in_bttn_x = self.l_x > bttn.x and self.l_x < (bttn.x + bttn.width)
        l_y_in_bttn_y = self.l_y > bttn.y and self.l_y < (bttn.y + bttn.height)
        l_in_bttn = l_x_in_bttn_x and l_y_in_bttn_y
        # Check if right hand in the area
        r_x_in_bttn_x = self.r_x > bttn.x and self.r_x < (bttn.x + bttn.width)
        r_y_in_bttn_y = self.r_y > bttn.y and self.r_y < (bttn.y + bttn.height)
        r_in_bttn = r_x_in_bttn_x and r_y_in_bttn_y
        return (l_in_bttn or r_in_bttn) and not self.some_bttn_active