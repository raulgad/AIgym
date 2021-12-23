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

        self.lhand_in_pause_bttn = False
        self.rhand_in_pause_bttn = False
        self.lhand_in_next_bttn = False
        self.rhand_in_next_bttn = False
        self.lhand_in_exit_butt = False
        self.rhand_in_exit_butt = False
        self.lhand_in_cont_butt = False
        self.rhand_in_cont_butt = False
        self.lhand_in_yoga_butt = False
        self.rhand_in_yoga_butt = False
        self.lhand_in_workout_butt = False
        self.rhand_in_workout_butt = False

        self.next_bttn_tapped = False
        self.pause_bttn_tapped = False
        self.exit_butt_tapped = False
        self.cont_butt_tapped = False
        self.yoga_butt_tapped = False
        self.workout_butt_tapped = False

        self.some_bttn_active = False
        
    def set_hands_coords(self, lmks):
        # Set current coordinates of left and right hands
        self.l_x, self.l_y, _ = lmks[cons.RIGHT_INDEX]
        self.r_x, self.r_y, _ = lmks[cons.LEFT_INDEX]
