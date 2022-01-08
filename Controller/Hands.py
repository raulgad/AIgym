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
