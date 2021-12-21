import cv2
import mediapipe as mp
import math
import json
import os
import time
import numpy as np
window_width = 960 #1024
window_height = 540 #768

dirname = os.path.dirname(__file__)

def draw_point(img, x, y, clr=(0,0,255)):
    cv2.circle(img, (x, y), 5, clr, cv2.FILLED)
    cv2.circle(img, (x, y), 10, clr, 2)

def draw_line(img, landmarks, points=[], clr=(255,255,255), point_clr=(255,255,255)):
    for p_idx, point in enumerate(points):
        # Draw point
        x1, y1, _ = landmarks[point]
        draw_point(img, x1, y1, clr=point_clr)
        # Draw line and next point
        if p_idx + 1 < len(points):
            x2, y2, _ = landmarks[points[p_idx + 1]]
            cv2.line(img, (x1, y1), (x2, y2), clr, 3)
            draw_point(img, x2, y2, clr=point_clr)

class poseDetector():
 
    def __init__(self, static_image_mode=False, model_complexity=0, smooth_landmarks=True, enable_segmentation=False, smooth_segmentation=True,
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):
        
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
 
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.static_image_mode, self.model_complexity, 
                                    self.smooth_landmarks, self.enable_segmentation, 
                                    self.smooth_segmentation, self.min_detection_confidence, 
                                    self.min_tracking_confidence)
        
        # Init poses dictionary from json file
        with open(os.path.join(dirname, 'poses.json'), 'r') as fp:
            self.poses = json.load(fp)

            # Convert angle's tuple to type 'typle' (from string)
            # TODO: Add END poses and others keys
            for _, pose in self.poses.items():
                pose['start']['angles'] = {eval(k):v for k,v in pose['start']['angles'].items()}

    def correct_pose(self, img, curr_lmks, angles, angle_gap = 20.0, draw=False):
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
                                    points=[ang_draw_ids[0], 
                                            ang_draw_ids[1], 
                                            ang_draw_ids[2]], 
                                    clr=(0,0,255))
            # Return true if all user angles is correct
            return curr_corr_count == len(angles)
        except:
            print('Something going wrong in correct_pose() -> PoseModule')
            return False
        
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img, self.results
 
    def findPosition(self, img):
        self.lmList = []
        try:
            if self.results.pose_landmarks:
                for lm in self.results.pose_landmarks.landmark:
                    h, w, _ = img.shape
                    cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    self.lmList.append([cx, cy, cz])
        except:
            pass
        return self.lmList
 
    def find_angle(self, ps, lmks):
        # Get the coordinates
        x1, y1, _ = lmks[ps[0]]
        x2, y2, _ = lmks[ps[1]]
        x3, y3, _ = lmks[ps[2]]
        # Calculate the Angle
        angle = abs(math.degrees(math.atan2(y3 - y2, x3 - x2) 
                                - math.atan2(y1 - y2, x1 - x2)))
        return angle

    def findAngle(self, ps):
        # Get the landmarks
        x1, y1, _ = self.lmList[ps[0]]
        x2, y2, _ = self.lmList[ps[1]]
        x3, y3, _ = self.lmList[ps[2]]
        # Calculate the Angle
        angle = abs(math.degrees(math.atan2(y3 - y2, x3 - x2) 
                            - math.atan2(y1 - y2, x1 - x2)))
        return angle

    def classifyPose(self):
        '''
        This function classifies yoga poses depending upon the angles of various body joints.
        Args:
            landmarks: A list of detected landmarks of the person whose pose needs to be classified.
            output_image: A image of the person with the detected pose landmarks drawn.
            display: A boolean value that is if set to true the function displays the resultant image with the pose label 
            written on it and returns nothing.
        Returns:
            output_image: The image with the detected pose landmarks drawn and pose label written.
            label: The classified pose label of the person in the output_image.
        '''
        
        # Initialize the label of the pose. It is not known at this stage.
        label = 'Unknown Pose'

        # Calculate the required angles.
        #----------------------------------------------------------------------------------------------------------------
        
        # Get the angle between the left shoulder, elbow and wrist points.
        left_elbow_angle = self.findAngle((self.mpPose.PoseLandmark.LEFT_SHOULDER.value, 
                                        self.mpPose.PoseLandmark.LEFT_ELBOW.value, 
                                        self.mpPose.PoseLandmark.LEFT_WRIST.value))

        # Get the angle between the right shoulder, elbow and wrist points. 
        right_elbow_angle = self.findAngle((self.mpPose.PoseLandmark.RIGHT_SHOULDER.value,
                                        self.mpPose.PoseLandmark.RIGHT_ELBOW.value,
                                        self.mpPose.PoseLandmark.RIGHT_WRIST.value))   
        
        # Get the angle between the left elbow, shoulder and hip points. 
        left_shoulder_angle = self.findAngle((self.mpPose.PoseLandmark.LEFT_ELBOW.value,
                                            self.mpPose.PoseLandmark.LEFT_SHOULDER.value,
                                            self.mpPose.PoseLandmark.LEFT_HIP.value))

        # Get the angle between the right hip, shoulder and elbow points. 
        right_shoulder_angle = self.findAngle((self.mpPose.PoseLandmark.RIGHT_HIP.value,
                                            self.mpPose.PoseLandmark.RIGHT_SHOULDER.value,
                                            self.mpPose.PoseLandmark.RIGHT_ELBOW.value))

        # Get the angle between the left hip, knee and ankle points. 
        left_knee_angle = self.findAngle((self.mpPose.PoseLandmark.LEFT_HIP.value,
                                        self.mpPose.PoseLandmark.LEFT_KNEE.value,
                                        self.mpPose.PoseLandmark.LEFT_ANKLE.value))

        # Get the angle between the right hip, knee and ankle points 
        right_knee_angle = self.findAngle((self.mpPose.PoseLandmark.RIGHT_HIP.value,
                                        self.mpPose.PoseLandmark.RIGHT_KNEE.value,
                                        self.mpPose.PoseLandmark.RIGHT_ANKLE.value))
        
        #----------------------------------------------------------------------------------------------------------------
        
        # Check if it is the warrior II pose or the T pose.
        # As for both of them, both arms should be straight and shoulders should be at the specific angle.
        #----------------------------------------------------------------------------------------------------------------
        
        # Check if the both arms are straight.
        if left_elbow_angle > 165 and left_elbow_angle < 195 and right_elbow_angle > 165 and right_elbow_angle < 195:

            # Check if shoulders are at the required angle.
            if left_shoulder_angle > 80 and left_shoulder_angle < 110 and right_shoulder_angle > 80 and right_shoulder_angle < 110:

        # Check if it is the warrior II pose.
        #----------------------------------------------------------------------------------------------------------------

                # Check if one leg is straight.
                if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:

                    # Check if the other leg is bended at the required angle.
                    if left_knee_angle > 90 and left_knee_angle < 120 or right_knee_angle > 90 and right_knee_angle < 120:

                        # Specify the label of the pose that is Warrior II pose.
                        label = 'Warrior Pose' 
                            
        #----------------------------------------------------------------------------------------------------------------
        
        # Check if it is the T pose.
        #----------------------------------------------------------------------------------------------------------------
        
                # Check if both legs are straight
                if left_knee_angle > 160 and left_knee_angle < 195 and right_knee_angle > 160 and right_knee_angle < 195:

                    # Specify the label of the pose that is tree pose.
                    label = 'T Pose'

        #----------------------------------------------------------------------------------------------------------------
        
        # Check if it is the tree pose.
        #----------------------------------------------------------------------------------------------------------------
        
        # Check if one leg is straight
        if left_knee_angle > 165 and left_knee_angle < 230 or right_knee_angle > 165 and right_knee_angle < 230:

            # Check if the other leg is bended at the required angle.
            if left_knee_angle > 315 and left_knee_angle < 360 or right_knee_angle > 15 and right_knee_angle < 75:
                
                # Specify the label of the pose that is tree pose.
                label = 'Tree Pose'
                    
        #----------------------------------------------------------------------------------------------------------------

        return label
        