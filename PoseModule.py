import cv2
import mediapipe as mp
import math
import json
import os
import Constants as cons

def draw_point(img, x, y, clr=cons.clr_red):
    cv2.circle(img, (x, y), cons.vw_train_circle_filled_rad, clr, cv2.FILLED)
    cv2.circle(img, (x, y), cons.vw_train_circle_rad, clr)

def draw_line(img, lmks, points=[], clr=cons.clr_white, point_clr=cons.clr_white):
    for p_idx, point in enumerate(points):
        # Draw point
        x1, y1, _ = lmks[point]
        draw_point(img, x1, y1, clr=point_clr)
        # Draw line to next point
        if p_idx + 1 < len(points):
            x2, y2, _ = lmks[points[p_idx + 1]]
            cv2.line(img, (x1, y1), (x2, y2), clr, cons.fnt_thick)
            draw_point(img, x2, y2, clr=point_clr)

class poseDetector():
 
    def __init__(self, static_image_mode=False, model_complexity=0, smooth_landmarks=True, 
                enable_segmentation=False, smooth_segmentation=True,
                min_detection_confidence=0.5, min_tracking_confidence=0.5):
        
        self.mpipepose = mp.solutions.pose.Pose(static_image_mode, model_complexity, 
                                    smooth_landmarks, enable_segmentation, 
                                    smooth_segmentation, min_detection_confidence, 
                                    min_tracking_confidence)
        
        # Init poses dictionary from json file
        with open(os.path.join(os.path.dirname(__file__), cons.file_poses), 'r') as fp:
            self.poses = json.load(fp)

            # Convert angle from string to tuple
            # TODO: Add END poses and others keys
            for _, pose in self.poses.items():
                pose['start']['angles'] = {eval(k):v for k,v in pose['start']['angles'].items()}

    def correct_pose(self, img, curr_lmks, angles, angle_gap = cons.ang_pose_detect_gap, draw=False):
        # Init variable of user's current correct angles
        curr_corr_count = 0
        # Init dictionary of user's current not correct angles
        angs_draw = {}
        try:
            # Check each current angle if it's same as correct
            for ang_ids, ang in angles.items():
                # Get current user's angle from it's points
                curr_ang = self.find_angle(ang_ids, curr_lmks)
                # Check if current user angle is in suitable range
                if abs(curr_ang - ang) <= angle_gap:
                    curr_corr_count += 1
                    # Remove the angle that has become correct, for not drawing it later
                    if ang_ids in angs_draw:
                        del angs_draw[ang_ids]
                # Add angle that user should do
                else:
                    curr_corr_count -= 1
                    angs_draw[ang_ids] = ang
                    #Draw correction if needed
                    if draw:
                        # Draw incorrect angle lines.
                        for ang_draw_ids, _ in angs_draw.items():
                            draw_line(img, curr_lmks, 
                                    points=[ang_draw_ids[0], ang_draw_ids[1], ang_draw_ids[2]], clr=cons.clr_red)
            # Return true if all user angles is correct
            return curr_corr_count == len(angles)
        except:
            print('Something goes wrong in correct_pose() -> PoseModule')
            return False
 
    def analyze(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.mpipepose.process(imgRGB)
        lmks = []
        try:
            if results.pose_landmarks:
                # Get coordinates of the landmarks according to the screen size
                for lm in results.pose_landmarks.landmark:
                    height, width, _ = img.shape
                    cx, cy, cz = int(lm.x * width), int(lm.y * height), int(lm.z * width)
                    lmks.append([cx, cy, cz])
        except:
            print('Something goes wrong in analyze() -> PoseModule')
            pass
        return lmks, results.segmentation_mask
 
    def find_angle(self, points, lmks):
        # Get the coordinates
        x1, y1, _ = lmks[points[0]]
        x2, y2, _ = lmks[points[1]]
        x3, y3, _ = lmks[points[2]]
        # Calculate the angle between three coordinates
        angle = abs(math.degrees(math.atan2(y3 - y2, x3 - x2) 
                                - math.atan2(y1 - y2, x1 - x2)))
        return angle

        