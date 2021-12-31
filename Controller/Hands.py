import logging
import Constants as cons
import Controller.Detector as detector

"""
Responsible for logic of remote hands controll
"""
l_x, l_y, r_x, r_y  = 0, 0, 0, 0

def set():
    # Set current coordinates of left (l) and right (r) hands
    global l_x, l_y, r_x, r_y
    if detector.lmks:
        try:
            l_x, l_y, _ = detector.lmks[cons.RIGHT_INDEX]
            r_x, r_y, _ = detector.lmks[cons.LEFT_INDEX]
        except:
            logging.debug('Cant set hands coordinates in set() -> Hands')
            pass
        

def point_between(point, between):
    return point > between[0] and point < (between[0] + between[1])

def focus(view) -> bool:
    # Return if user hand in button area and some other button isnt active
    view_horiz = (view.x, view.width)
    view_vert = (view.y, view.height)
    # Check if left hand in the area
    l_in_view = point_between(l_x, view_horiz) and point_between(l_y, view_vert)
    # Check if right hand in the area
    r_in_view = point_between(r_x, view_horiz) and point_between(r_y, view_vert)
    return l_in_view or r_in_view

# class ControllerHands:
    # """
    # Responsible for the logic of remote hands controll
    # """

#     def __init__(self):
#         self.pause_bttn_active = True
#         self.next_bttn_active = True
#         self.exit_butt_active = False
#         self.cont_butt_active = False
#         self.yoga_butt_active = True
#         self.workout_butt_active = True

#         # self.lhand_in_pause_bttn = False
#         # self.rhand_in_pause_bttn = False
#         # self.lhand_in_next_bttn = False
#         # self.rhand_in_next_bttn = False
#         # self.lhand_in_exit_butt = False
#         # self.rhand_in_exit_butt = False
#         # self.lhand_in_cont_butt = False
#         # self.rhand_in_cont_butt = False
#         # self.lhand_in_yoga_butt = False
#         # self.rhand_in_yoga_butt = False
#         # self.lhand_in_workout_butt = False
#         # self.rhand_in_workout_butt = False

#         self.next_bttn_tapped = False
#         self.pause_bttn_tapped = False
#         self.exit_butt_tapped = False
#         self.cont_butt_tapped = False
#         self.yoga_butt_tapped = False
#         self.workout_butt_tapped = False

#         self.some_view_active = False
        
#     def set(self, lmks):
#         # Set current coordinates of left (l) and right (r) hands
#         if lmks:
#             self.l_x, self.l_y, _ = lmks[cons.RIGHT_INDEX]
#             self.r_x, self.r_y, _ = lmks[cons.LEFT_INDEX]

#     def point_between(self, point, between):
#         return point > between[0] and point < (between[0] + between[1])

#     def focus(self, view) -> bool:
#         # Return if user hand in button area and some other button isnt active
#         view_horiz = (view.x, view.width)
#         view_vert = (view.y, view.height)
#         # Check if left hand in the area
#         l_in_view = self.point_between(self.l_x, view_horiz) and self.point_between(self.l_y, view_vert)
#         # Check if right hand in the area
#         r_in_view = self.point_between(self.r_x, view_horiz) and self.point_between(self.r_y, view_vert)
#         return (l_in_view or r_in_view) and not self.some_view_active