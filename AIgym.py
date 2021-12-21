import cv2
import numpy as np
import time
import PoseModule as pm
import os

dirname = os.path.dirname(__file__)

cap = cv2.VideoCapture(0)
window_width = 960 #1024
window_height = 540 #768
cap.set(3,window_width)
cap.set(4,window_height)

enable_segmentation=True

detector = pm.poseDetector(enable_segmentation=enable_segmentation)
count = 0
dir = 0
pTime = 0

black_clr = (0, 0, 0)
white_clr = (255, 255, 255)
green_clr = (0, 255, 0)
red_clr = (0, 0, 255)
blue_clr = (255, 0, 0)

# Init variables for first pose 
trng_seq = list(detector.poses)
#TODO: Get trng duration from json
trng_duration = 5 * 60 # mins, secs
pose_name = trng_seq.pop(0)
pose_duration = detector.poses[pose_name]['duration']
pose_angles = detector.poses[pose_name]['start']['angles']



is_corr_pose = False
# is_corr_pose = 'Unknown Pose'
label_next_pose = 'T Pose'

wtimer_left = trng_duration
wtimer_text_size = 2
wtimer_curr_rec_width = 0
winit_time = time.time()
prev_wcurr_time = 0
wmins, wsecs = divmod(wtimer_left, 60)
wtimer = '{:02d}:{:02d}'.format(wmins, wsecs)

ptimer_left = pose_duration
ptimer_curr_rec_width = 0
pinit_time = time.time()
prev_pcurr_time = 0

wtimer_tapped = False
wtimer_active = True
wtimer_show = True
ptimer_active = True
ptimer_show = True

exit_butt_active = False
cont_butt_active = False

yoga_butt_active = True
workout_butt_active = True

yoga_active = False
workout_active = False

winit_time = time.time()
wcurr_time = 0

pinit_time = time.time()
pcurr_time = 0

hand_in_wtimer_inittime = time.time()
hand_in_wtimer_curr_time = 0

hand_in_exit_butt_inittime = time.time()
hand_in_exit_butt_curr_time = 0

hand_in_cont_butt_inittime = time.time()
hand_in_cont_butt_curr_time = 0

hand_in_ptimer_inittime = time.time()
hand_in_ptimer_curr_time = 0

hand_in_yoga_butt_inittime = time.time()
hand_in_yoga_butt_curr_time = 0

hand_in_workout_butt_inittime = time.time()
hand_in_workout_butt_curr_time = 0

lhand_in_wtimer = False
rhand_in_wtimer = False
lhand_in_ptimer = False
rhand_in_ptimer = False
lhand_in_exit_butt = False
rhand_in_exit_butt = False
lhand_in_cont_butt = False
rhand_in_cont_butt = False
lhand_in_yoga_butt = False
rhand_in_yoga_butt = False
lhand_in_workout_butt = False
rhand_in_workout_butt = False

ptimer_pressed = False
wtimer_pressed = False
exit_butt_pressed = False
cont_butt_pressed = False
yoga_butt_pressed = False
workout_butt_pressed = False

# Indexes of all landmarks
NOSE = detector.mpPose.PoseLandmark.NOSE.value
LEFT_EYE_INNER = detector.mpPose.PoseLandmark.LEFT_EYE_INNER.value
LEFT_EYE = detector.mpPose.PoseLandmark.LEFT_EYE.value
LEFT_EYE_OUTER = detector.mpPose.PoseLandmark.LEFT_EYE_OUTER.value
RIGHT_EYE_INNER = detector.mpPose.PoseLandmark.RIGHT_EYE_INNER.value
RIGHT_EYE = detector.mpPose.PoseLandmark.RIGHT_EYE.value
RIGHT_EYE_OUTER = detector.mpPose.PoseLandmark.RIGHT_EYE_OUTER.value
LEFT_EAR = detector.mpPose.PoseLandmark.LEFT_EAR.value
RIGHT_EAR = detector.mpPose.PoseLandmark.RIGHT_EAR.value
MOUTH_LEFT = detector.mpPose.PoseLandmark.MOUTH_LEFT.value
MOUTH_RIGHT = detector.mpPose.PoseLandmark.MOUTH_RIGHT.value
LEFT_SHOULDER = detector.mpPose.PoseLandmark.LEFT_SHOULDER.value
RIGHT_SHOULDER = detector.mpPose.PoseLandmark.RIGHT_SHOULDER.value
LEFT_ELBOW = detector.mpPose.PoseLandmark.LEFT_ELBOW.value
RIGHT_ELBOW = detector.mpPose.PoseLandmark.RIGHT_ELBOW.value
LEFT_WRIST = detector.mpPose.PoseLandmark.LEFT_WRIST.value
RIGHT_WRIST = detector.mpPose.PoseLandmark.RIGHT_WRIST.value
LEFT_PINKY = detector.mpPose.PoseLandmark.LEFT_PINKY.value
RIGHT_PINKY = detector.mpPose.PoseLandmark.RIGHT_PINKY.value
LEFT_INDEX = detector.mpPose.PoseLandmark.LEFT_INDEX.value
RIGHT_INDEX = detector.mpPose.PoseLandmark.RIGHT_INDEX.value
LEFT_THUMB = detector.mpPose.PoseLandmark.LEFT_THUMB.value
RIGHT_THUMB = detector.mpPose.PoseLandmark.RIGHT_THUMB.value
LEFT_HIP = detector.mpPose.PoseLandmark.LEFT_HIP.value
RIGHT_HIP = detector.mpPose.PoseLandmark.RIGHT_HIP.value
LEFT_KNEE = detector.mpPose.PoseLandmark.LEFT_KNEE.value
RIGHT_KNEE = detector.mpPose.PoseLandmark.RIGHT_KNEE.value
LEFT_ANKLE = detector.mpPose.PoseLandmark.LEFT_ANKLE.value
RIGHT_ANKLE = detector.mpPose.PoseLandmark.RIGHT_ANKLE.value
LEFT_HEEL = detector.mpPose.PoseLandmark.LEFT_HEEL.value
RIGHT_HEEL = detector.mpPose.PoseLandmark.RIGHT_HEEL.value
LEFT_FOOT_INDEX = detector.mpPose.PoseLandmark.LEFT_FOOT_INDEX.value
RIGHT_FOOT_INDEX = detector.mpPose.PoseLandmark.RIGHT_FOOT_INDEX.value

# Indexes of landmarks for pose classification and correction
main_lnms = [LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_ELBOW, RIGHT_ELBOW,
            LEFT_WRIST, RIGHT_WRIST, LEFT_HIP, RIGHT_HIP, LEFT_KNEE,
            RIGHT_KNEE, LEFT_ANKLE, RIGHT_ANKLE]


# def drawPoints(img, landmarks, points=[]):
#     points.sort()
#     for p_idx, point in enumerate(points):
#         # Draw point
#         x1, y1, _ = landmarks[point]
#         drawCircle(img, x1, y1)
#         # Draw line and next point
#         next_p_idx = p_idx + 1
#         if next_p_idx < len(points):
#             next_point = points[next_p_idx]
#             x2, y2, _ = landmarks[next_point]
#             cv2.line(img, (x1, y1), (x2, y2), white_clr, 3)
#             drawCircle(img, x2, y2)
#             # Draw angle
#             if next_p_idx + 1 < len(points):
#                 angle = detector.findAngle((point, next_point, points[next_p_idx + 1]))
#                 cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, white_clr, 2)

# def drawCircle(img, x, y, clr = red_clr):
#     cv2.circle(img, (x, y), 10, clr, cv2.FILLED)
#     cv2.circle(img, (x, y), 15, clr, 2)

# # Congrats
# img_glasses = cv2.imread(os.path.join(dirname, 'imgs/glasses_cig.png'), cv2.IMREAD_UNCHANGED)
# img_glasses = cv2.resize(img_glasses, (0, 0), None, 0.25, 0.25)
# img_cows = cv2.imread(os.path.join(dirname, 'imgs/cows.jpg'), cv2.IMREAD_UNCHANGED)
# img_cows = cv2.resize(img_cows,(window_width,window_height))

# def overlayPNG(imgBack, imgFront, pos=[0, 0]):
#     hf, wf, cf = imgFront.shape
#     hb, wb, cb = imgBack.shape
#     *_, mask = cv2.split(imgFront)
#     maskBGRA = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
#     maskBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
#     imgRGBA = cv2.bitwise_and(imgFront, maskBGRA)
#     imgRGB = cv2.cvtColor(imgRGBA, cv2.COLOR_BGRA2BGR)

#     imgMaskFull = np.zeros((hb, wb, cb), np.uint8)
#     imgMaskFull2 = np.ones((hb, wb, cb), np.uint8) * 255

#     try:
#         imgMaskFull[pos[1]:hf + pos[1], pos[0]:wf + pos[0], :] = imgRGB
#         maskBGRInv = cv2.bitwise_not(maskBGR)
#         imgMaskFull2[pos[1]:hf + pos[1], pos[0]:wf + pos[0], :] = maskBGRInv
#     except:
#         pass

#     imgBack = cv2.bitwise_and(imgBack, imgMaskFull2)
#     imgBack = cv2.bitwise_or(imgBack, imgMaskFull)

    # return imgBack

# Background video 
bg_video_name = os.path.join(dirname, 'pose_1.mp4')
capBackground = cv2.VideoCapture(bg_video_name)
capBackground.set(3,window_height)
capBackground.set(4,window_width)

cv2.namedWindow('AIgym', cv2.WINDOW_NORMAL)

while cap.isOpened():
    _, img = cap.read()

    # Flip the frame horizontally for natural (selfie-view) visualization.
    img = cv2.flip(img, 1)

    img, results = detector.findPose(img, draw=False)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        
        # Hands Menu Control
        lhand_x, lhand_y, _ = lmList[RIGHT_INDEX]
        rhand_x, rhand_y, _ = lmList[LEFT_INDEX]


        # Youga
        if yoga_active:

            # Right Arm
            angle = detector.findAngle((RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST))


            # drawPoints(img, lmList, points=[NOSE])
            # drawPoints(img, lmList, points=[RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST])


            per = np.interp(angle, (210, 310), (0, 100))
            bar = np.interp(angle, (220, 310), (450, 100))
    
            # Check for the dumbbell curls
            color = (255, 0, 255)
            if per == 100:
                color = (0, 255, 0)
                if dir == 0:
                    count += 0.5
                    dir = 1
            if per == 0:
                color = (0, 255, 0)
                if dir == 1:
                    count += 0.5
                    dir = 0
            # print(count)


            # TODO: Try to use async
            # Segmentation
            if enable_segmentation:
                # Read background video frame
                success, img_back = capBackground.read()
                # Repeat video if it's end
                if not success:
                    capBackground.set(1, 0)
                else:
                    # TODO: Use video with correct resolution
                    # Resize video frame to be equal window's size
                    img_back = cv2.resize(img_back,(window_width,window_height),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
                    # Add background frame to segmented user's frame
                    condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
                    bg_image = np.zeros(img.shape, dtype=np.uint8)
                    bg_image[:] = img_back
                    img = np.where(condition, img, bg_image)


            # Perform Pose landmark detection.
            # is_corr_pose = detector.classifyPose()

            

            is_corr_pose = detector.correct_pose(img, lmList, pose_angles, draw=True)
            
            # if res:
            #     print(time_end - time_start)


            # Exersize sequence

            # Update the color (to green) with which the label will be written on the image.
            label_clr = green_clr if is_corr_pose or label_next_pose == 'Done!' else red_clr

            # Write the label on the output image. 
            cv2.putText(img, label_next_pose, (400, 75),cv2.FONT_HERSHEY_PLAIN, 2, label_clr, 2)
            


            # Workout timer

            wtimer_pos_x = 10
            wtimer_pos_y = 10
            wtimer_width = 300
            wtimer_height = 100
            wtimer_width_step = wtimer_width / trng_duration

            if wtimer_active:
                
                if wtimer_left > 0:
                    wcurr_time = int(time.time() - winit_time)

                    if prev_wcurr_time != wcurr_time:
                        wtimer_curr_rec_width += int(wtimer_width_step)
                        prev_wcurr_time = wcurr_time
                        wtimer_left -= 1

                        wmins, wsecs = divmod(wtimer_left, 60)
                        wtimer = '{:02d}:{:02d}'.format(wmins, wsecs)
                else:
                    wtimer= 'Time is end!'
                    wtimer_text_size = 1
                    winit_time = time.time()
            else:
                winit_time = time.time()

            if wtimer_show:
                #Draw workout timer
                cv2.rectangle(img, 
                            (wtimer_pos_x, wtimer_pos_y), 
                            (wtimer_pos_x + wtimer_width, wtimer_pos_y + wtimer_height), 
                            black_clr, 
                            3)

                if wtimer_left > 0:
                    cv2.rectangle(img, 
                                (wtimer_pos_x, wtimer_pos_y), 
                                (wtimer_pos_x + wtimer_curr_rec_width, wtimer_pos_y + wtimer_height), 
                                black_clr, 
                                cv2.FILLED)
                else:
                    cv2.rectangle(img, 
                                (wtimer_pos_x, wtimer_pos_y), 
                                (wtimer_pos_x + wtimer_width, wtimer_pos_y + wtimer_height), 
                                black_clr, 
                                cv2.FILLED)
                
                #Workout timer text
                cv2.putText(img, 
                            'Pause', 
                            (wtimer_pos_x + 5, wtimer_pos_y + 65), 
                            cv2.FONT_HERSHEY_DUPLEX, 
                            1, 
                            white_clr, 
                            2)
                cv2.putText(img, 
                            wtimer, 
                            (wtimer_pos_x + 115, wtimer_pos_y + 65), 
                            cv2.FONT_HERSHEY_DUPLEX, 
                            wtimer_text_size, 
                            white_clr, 
                            2)

            
            #Pose timer
            ptimer_pos_y = 10
            ptimer_width = 300
            ptimer_height = 100
            ptimer_pos_x = 650  # window_width - ptimer_width - 10
            ptimer_width_step = ptimer_width / pose_duration
            ptimer_text = 'Next'
            
            # Change pose timer button if it's active
            if ptimer_active:
                # Change anything only if we detect any pose
                if is_corr_pose:
                    # Fill pose timer button by increasing filled button's rectangle each time when
                    # we current pose is equal label_next_pose and when pose timer is not end.
                    if ptimer_left > 0 and is_corr_pose:
                        # Calculate time that starts right after we detect correct pose (label == label_next_pose)
                        pcurr_time = int(time.time() - pinit_time)
                        # Change filled pose timer rectangle each second. One second is 
                        # passed when 'prev_pcurr_time != pcurr_time'
                        if prev_pcurr_time != pcurr_time:
                            # Increase filled pose timer rectangle for one time (+ ptimer_curr_rec_width)
                            ptimer_curr_rec_width += int(ptimer_width_step)
                            # Save current pose time (pcurr_time) to prev_pcurr_time for detect 
                            #  when 1 second is passed
                            prev_pcurr_time = pcurr_time
                            # Update timer that indicates how much time is left to end the pose.
                            ptimer_left -= 1
                    
                    elif ptimer_left <= 0:
                        # Reset timers and pose label if pose time is ended.
                        ptimer_left = pose_duration
                        ptimer_curr_rec_width = 0

                        
                        
                        # Check if user is done training
                        if not trng_seq:
                            label_next_pose = 'Done!'
                            ptimer_active = False
                        # Reset pose variables to next pose
                        elif is_corr_pose:
                            is_corr_pose = False
                            
                            # Set next pose
                            pose_name = trng_seq.pop(0)
                            # Set new values to pose variables 
                            label_next_pose = pose_name.capitalize() + ' Pose'
                            pose_duration = detector.poses[pose_name]['duration']
                            pose_angles = detector.poses[pose_name]['start']['angles']
                            
                    
                            

                        # if label_next_pose == trng_seq[0].capitalize() + ' Pose':
                        #     label_next_pose = trng_seq[1].capitalize() + ' Pose'
                        # elif label_next_pose == trng_seq[1].capitalize() + ' Pose':
                        #     label_next_pose = trng_seq[2].capitalize() + ' Pose'
                        # elif label_next_pose == trng_seq[2].capitalize() + ' Pose':
                        #     label_next_pose = 'Done!'

                else:
                    pinit_time = time.time()


            if ptimer_show:
                cv2.rectangle(img, 
                            (ptimer_pos_x, ptimer_pos_y), 
                            (ptimer_pos_x + ptimer_width, ptimer_pos_y + ptimer_height), 
                            black_clr, 
                            3)

                if ptimer_left > 0:
                    cv2.rectangle(img, 
                                (ptimer_pos_x, ptimer_pos_y), 
                                (ptimer_pos_x + ptimer_curr_rec_width, ptimer_pos_y + ptimer_height), 
                                black_clr, 
                                cv2.FILLED)
                else:
                    cv2.rectangle(img, 
                                (ptimer_pos_x, ptimer_pos_y), 
                                (ptimer_pos_x + ptimer_width, ptimer_pos_y + ptimer_height), 
                                black_clr, 
                                cv2.FILLED)
                
                #Workout timer text
                cv2.putText(img, 
                            ptimer_text, 
                            (ptimer_pos_x + 100, ptimer_pos_y + 65), 
                            cv2.FONT_HERSHEY_DUPLEX, 
                            1, 
                            white_clr, 
                            2)
            
            
            # Wtimer
            if wtimer_active:
                lhand_x_in_wtimer_x = lhand_x > wtimer_pos_x and lhand_x < (wtimer_pos_x + wtimer_width)
                lhand_y_in_wtimer_y = lhand_y > wtimer_pos_y and lhand_y < (wtimer_pos_y + wtimer_height)
                lhand_in_wtimer = lhand_x_in_wtimer_x and lhand_y_in_wtimer_y

                rhand_x_in_wtimer_x = rhand_x > wtimer_pos_x and rhand_x < (wtimer_pos_x + wtimer_width)
                rhand_y_in_wtimer_y = rhand_y > wtimer_pos_y and rhand_y < (wtimer_pos_y + wtimer_height)
                rhand_in_wtimer = rhand_x_in_wtimer_x and rhand_y_in_wtimer_y

                if (lhand_in_wtimer or rhand_in_wtimer) and not (lhand_in_ptimer or rhand_in_ptimer):
                    cv2.rectangle(img, 
                                (wtimer_pos_x, wtimer_pos_y), 
                                (wtimer_pos_x + wtimer_width, wtimer_pos_y + wtimer_height), 
                                green_clr, 
                                3)

                    # Detect 'tap' on wtimer
                    hand_in_wtimer_curr_time = int(time.time() - hand_in_wtimer_inittime)
                    if hand_in_wtimer_curr_time >= 1 and not wtimer_pressed:

                        wtimer_tapped = True
                        exit_butt_active = True
                        cont_butt_active = True
                        
                        cv2.rectangle(img, 
                                (wtimer_pos_x, wtimer_pos_y), 
                                (wtimer_pos_x + wtimer_width, wtimer_pos_y + wtimer_height), 
                                green_clr, 
                                cv2.FILLED)

                        wtimer_pressed = True
                else:
                    hand_in_wtimer_inittime = time.time()
                    wtimer_pressed = False

            # Draw pause buttons
            if wtimer_tapped:
                
                # Deactivate wtimer and ptimer buttons
                wtimer_active = False
                ptimer_active = False

                # Exit button
                if exit_butt_active:
                    
                    # Draw exit button
                    exit_butt_pos_x = int(window_width / 5.5)
                    exit_butt_pos_y = 200
                    exit_butt_width = 300
                    exit_butt_height = 100

                    cv2.rectangle(img, 
                                (exit_butt_pos_x, exit_butt_pos_y), 
                                (exit_butt_pos_x + exit_butt_width, exit_butt_pos_y + exit_butt_height), 
                                black_clr, 
                                3)
                    cv2.rectangle(img, 
                                (exit_butt_pos_x, exit_butt_pos_y), 
                                (exit_butt_pos_x + exit_butt_width, exit_butt_pos_y + exit_butt_height), 
                                black_clr, 
                                cv2.FILLED)
                    
                    # Exit button text
                    cv2.putText(img, 
                                'Exit', 
                                (exit_butt_pos_x + 100, exit_butt_pos_y + 65), 
                                cv2.FONT_HERSHEY_DUPLEX, 
                                1, 
                                white_clr, 
                                2)

                    lhand_x_in_exit_butt_x = lhand_x > exit_butt_pos_x and lhand_x < (exit_butt_pos_x + exit_butt_width)
                    lhand_y_in_exit_butt_y = lhand_y > exit_butt_pos_y and lhand_y < (exit_butt_pos_y + exit_butt_height)
                    lhand_in_exit_butt = lhand_x_in_exit_butt_x and lhand_y_in_exit_butt_y

                    rhand_x_in_exit_butt_x = rhand_x > exit_butt_pos_x and rhand_x < (exit_butt_pos_x + exit_butt_width)
                    rhand_y_in_exit_butt_y = rhand_y > exit_butt_pos_y and rhand_y < (exit_butt_pos_y + exit_butt_height)
                    rhand_in_exit_butt = rhand_x_in_exit_butt_x and rhand_y_in_exit_butt_y

                    if (lhand_in_exit_butt or rhand_in_exit_butt) and not (lhand_in_cont_butt or rhand_in_cont_butt):
                        cv2.rectangle(img, 
                                    (exit_butt_pos_x, exit_butt_pos_y), 
                                    (exit_butt_pos_x + exit_butt_width, exit_butt_pos_y + exit_butt_height), 
                                    green_clr, 
                                    3)

                        # Detect 'tap' on exit_butt
                        hand_in_exit_butt_curr_time = int(time.time() - hand_in_exit_butt_inittime)
                        if hand_in_exit_butt_curr_time >= 1 and not exit_butt_pressed:

                            cv2.rectangle(img, 
                                    (exit_butt_pos_x, exit_butt_pos_y), 
                                    (exit_butt_pos_x + exit_butt_width, exit_butt_pos_y + exit_butt_height), 
                                    green_clr, 
                                    cv2.FILLED)
                            
                            exit_butt_active = False
                            wtimer_tapped = False
                            yoga_active = False
                            yoga_butt_active = True
                            workout_butt_active = True

                            exit_butt_pressed = True

                    else:
                        hand_in_exit_butt_inittime = time.time()
                        exit_butt_pressed = False
                
                

                # Cont button
                if cont_butt_active:
                    # Draw continue button
                    cont_butt_pos_x = exit_butt_pos_x + exit_butt_width + 60
                    cont_butt_pos_y = 200
                    cont_butt_width = 300
                    cont_butt_height = 100

                    cv2.rectangle(img, 
                                (cont_butt_pos_x, cont_butt_pos_y), 
                                (cont_butt_pos_x + cont_butt_width, cont_butt_pos_y + cont_butt_height), 
                                black_clr, 
                                3)
                    cv2.rectangle(img, 
                                (cont_butt_pos_x, cont_butt_pos_y), 
                                (cont_butt_pos_x + cont_butt_width, cont_butt_pos_y + cont_butt_height), 
                                black_clr, 
                                cv2.FILLED)
                    
                    # Exit button text
                    cv2.putText(img, 'Continue', (cont_butt_pos_x + 80, cont_butt_pos_y + 65), cv2.FONT_HERSHEY_DUPLEX, 1, 
                                white_clr, 2)

                    lhand_x_in_cont_butt_x = lhand_x > cont_butt_pos_x and lhand_x < (cont_butt_pos_x + cont_butt_width)
                    lhand_y_in_cont_butt_y = lhand_y > cont_butt_pos_y and lhand_y < (cont_butt_pos_y + cont_butt_height)
                    lhand_in_cont_butt = lhand_x_in_cont_butt_x and lhand_y_in_cont_butt_y

                    rhand_x_in_cont_butt_x = rhand_x > cont_butt_pos_x and rhand_x < (cont_butt_pos_x + cont_butt_width)
                    rhand_y_in_cont_butt_y = rhand_y > cont_butt_pos_y and rhand_y < (cont_butt_pos_y + cont_butt_height)
                    rhand_in_cont_butt = rhand_x_in_cont_butt_x and rhand_y_in_cont_butt_y

                    if (lhand_in_cont_butt or rhand_in_cont_butt) and not (lhand_in_exit_butt or rhand_in_exit_butt):
                        cv2.rectangle(img, 
                                    (cont_butt_pos_x, cont_butt_pos_y), 
                                    (cont_butt_pos_x + cont_butt_width, cont_butt_pos_y + cont_butt_height), 
                                    green_clr, 
                                    3)

                        # Detect 'tap' on cont_butt
                        hand_in_cont_butt_curr_time = int(time.time() - hand_in_cont_butt_inittime)
                        if hand_in_cont_butt_curr_time >= 1 and not cont_butt_pressed:
                            
                            cont_butt_active = False
                            wtimer_tapped = False
                            wtimer_active = True
                            ptimer_active = True

                            cv2.rectangle(img, 
                                    (cont_butt_pos_x, cont_butt_pos_y), 
                                    (cont_butt_pos_x + cont_butt_width, cont_butt_pos_y + cont_butt_height), 
                                    green_clr, 
                                    cv2.FILLED)

                            cont_butt_pressed = True

                    else:
                        hand_in_cont_butt_inittime = time.time()
                        cont_butt_pressed = False


            # Ptimer
            if ptimer_active:
                lhand_x_in_ptimer_x = lhand_x > ptimer_pos_x and lhand_x < (ptimer_pos_x + ptimer_width)
                lhand_y_in_ptimer_y = lhand_y > ptimer_pos_y and lhand_y < (ptimer_pos_y + ptimer_height)
                lhand_in_ptimer = lhand_x_in_ptimer_x and lhand_y_in_ptimer_y

                rhand_x_in_ptimer_x = rhand_x > ptimer_pos_x and rhand_x < (ptimer_pos_x + ptimer_width)
                rhand_y_in_ptimer_y = rhand_y > ptimer_pos_y and rhand_y < (ptimer_pos_y + ptimer_height)
                rhand_in_ptimer = rhand_x_in_ptimer_x and rhand_y_in_ptimer_y

                if (lhand_in_ptimer or rhand_in_ptimer) and not (lhand_in_wtimer or rhand_in_wtimer):
                    cv2.rectangle(img, 
                                (ptimer_pos_x, ptimer_pos_y), 
                                (ptimer_pos_x + ptimer_width, ptimer_pos_y + ptimer_height), 
                                green_clr, 
                                3)

                    # Detect 'tap' on ptimer
                    hand_in_ptimer_curr_time = int(time.time() - hand_in_ptimer_inittime)
                    if hand_in_ptimer_curr_time >= 1 and not ptimer_pressed:
                        
                        ptimer_left = pose_duration
                        ptimer_curr_rec_width = 0
                        
                        #TODO: DRY
                        # Check if user is done training
                        if not trng_seq:
                            label_next_pose = 'Done!'
                            ptimer_active = False

                        # Reset pose variables to next pose
                        else:

                            # Set next pose
                            pose_name = trng_seq.pop(0)
                            # Set new values to pose variables 
                            label_next_pose = pose_name.capitalize() + ' Pose'
                            pose_duration = detector.poses[pose_name]['duration']
                            pose_angles = detector.poses[pose_name]['start']['angles']


                        cv2.rectangle(img, 
                                (ptimer_pos_x, ptimer_pos_y), 
                                (ptimer_pos_x + ptimer_width, ptimer_pos_y + ptimer_height), 
                                green_clr, 
                                cv2.FILLED)

                        ptimer_pressed = True

                else:
                    hand_in_ptimer_inittime = time.time()
                    ptimer_pressed = False

        
        # # Draw congrats
        # if label_next_pose == 'Done!':
            
        #     # TODO: DRY
        #     # Add background frame to segmented user's frame
        #     condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        #     bg_image = np.zeros(img.shape, dtype=np.uint8)
        #     bg_image[:] = img_cows
        #     img = np.where(condition, img, bg_image)

        #     reye_x, reye_y, _ = lmList[RIGHT_EYE_OUTER]
        #     leye_x, leye_y, _ = lmList[LEFT_EYE_OUTER]

        #     # Resize glasses relative to depth (changed distance between eyes)
        #     glasses_w = abs(int((leye_x - reye_x) * 1.3))
        #     glasses_h = int(glasses_w * 1.05)
        #     img_glasses = cv2.resize(img_glasses, (glasses_w, glasses_h),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)

        #     img = overlayPNG(img, img_glasses, [reye_x - 20, reye_y])


        # Menu buttons
        if yoga_butt_active:
            # Draw yoga button
            yoga_butt_pos_x = 10
            yoga_butt_pos_y = 10
            yoga_butt_width = 300
            yoga_butt_height = 100

            cv2.rectangle(img, 
                        (yoga_butt_pos_x, yoga_butt_pos_y), 
                        (yoga_butt_pos_x + yoga_butt_width, yoga_butt_pos_y + yoga_butt_height), 
                        black_clr, 
                        3)
            cv2.rectangle(img, 
                        (yoga_butt_pos_x, yoga_butt_pos_y), 
                        (yoga_butt_pos_x + yoga_butt_width, yoga_butt_pos_y + yoga_butt_height), 
                        black_clr, 
                        cv2.FILLED)
            
            # yoga button text
            cv2.putText(img, 
                        'Yoga', 
                        (yoga_butt_pos_x + 100, yoga_butt_pos_y + 65), 
                        cv2.FONT_HERSHEY_DUPLEX, 
                        1, 
                        white_clr, 
                        2)

            # Tap yoga button
            if yoga_butt_active:
                lhand_x_in_yoga_butt_x = lhand_x > yoga_butt_pos_x and lhand_x < (yoga_butt_pos_x + yoga_butt_width)
                lhand_y_in_yoga_butt_y = lhand_y > yoga_butt_pos_y and lhand_y < (yoga_butt_pos_y + yoga_butt_height)
                lhand_in_yoga_butt = lhand_x_in_yoga_butt_x and lhand_y_in_yoga_butt_y

                rhand_x_in_yoga_butt_x = rhand_x > yoga_butt_pos_x and rhand_x < (yoga_butt_pos_x + yoga_butt_width)
                rhand_y_in_yoga_butt_y = rhand_y > yoga_butt_pos_y and rhand_y < (yoga_butt_pos_y + yoga_butt_height)
                rhand_in_yoga_butt = rhand_x_in_yoga_butt_x and rhand_y_in_yoga_butt_y

                if (lhand_in_yoga_butt or rhand_in_yoga_butt) and not (lhand_in_workout_butt or rhand_in_workout_butt):
                    cv2.rectangle(img, 
                                (yoga_butt_pos_x, yoga_butt_pos_y), 
                                (yoga_butt_pos_x + yoga_butt_width, yoga_butt_pos_y + yoga_butt_height), 
                                green_clr, 
                                3)

                    # Detect 'tap' on yoga_butt
                    hand_in_yoga_butt_curr_time = int(time.time() - hand_in_yoga_butt_inittime)
                    if hand_in_yoga_butt_curr_time >= 1 and not yoga_butt_pressed:
                        
                        # Reset to yoga
                        hand_in_wtimer_inittime = 1000000000000
                        hand_in_ptimer_inittime = 1000000000000

                        label_next_pose = 'T Pose'

                        wtimer_left = trng_duration
                        wtimer_text_size = 2
                        wtimer_curr_rec_width = 0
                        winit_time = time.time()
                        prev_wcurr_time = 0
                        wmins, wsecs = divmod(wtimer_left, 60)
                        wtimer = '{:02d}:{:02d}'.format(wmins, wsecs)

                        ptimer_left = pose_duration
                        ptimer_curr_rec_width = 0
                        pinit_time = time.time()
                        prev_pcurr_time = 0

                        wtimer_tapped = False
                        wtimer_active = True
                        wtimer_show = True
                        ptimer_active = True
                        ptimer_show = True

                        exit_butt_active = False
                        cont_butt_active = False

                        yoga_butt_active = False
                        workout_butt_active = False

                        yoga_active = True
                        workout_active = False
                        
                        yoga_butt_pressed = True

                        cv2.rectangle(img, 
                                (yoga_butt_pos_x, yoga_butt_pos_y), 
                                (yoga_butt_pos_x + yoga_butt_width, yoga_butt_pos_y + yoga_butt_height), 
                                green_clr, 
                                cv2.FILLED)

                else:
                    hand_in_yoga_butt_inittime = time.time()
                    yoga_butt_pressed = False

        if workout_butt_active:
            # Draw workout button
            workout_butt_pos_x = 650 #yoga_butt_pos_x + yoga_butt_width + 40
            workout_butt_pos_y = 10
            workout_butt_width = 300
            workout_butt_height = 100

            cv2.rectangle(img, 
                        (workout_butt_pos_x, workout_butt_pos_y), 
                        (workout_butt_pos_x + workout_butt_width, workout_butt_pos_y + workout_butt_height), 
                        black_clr, 
                        3)
            cv2.rectangle(img, 
                        (workout_butt_pos_x, workout_butt_pos_y), 
                        (workout_butt_pos_x + workout_butt_width, workout_butt_pos_y + workout_butt_height), 
                        black_clr, 
                        cv2.FILLED)
            
            # workout button text
            cv2.putText(img, 
                        'Workout', 
                        (workout_butt_pos_x + 100, workout_butt_pos_y + 65), 
                        cv2.FONT_HERSHEY_DUPLEX, 
                        1, 
                        white_clr, 
                        2)

            # Tap workout button
            if workout_butt_active:
                lhand_x_in_workout_butt_x = lhand_x > workout_butt_pos_x and lhand_x < (workout_butt_pos_x + workout_butt_width)
                lhand_y_in_workout_butt_y = lhand_y > workout_butt_pos_y and lhand_y < (workout_butt_pos_y + workout_butt_height)
                lhand_in_workout_butt = lhand_x_in_workout_butt_x and lhand_y_in_workout_butt_y

                rhand_x_in_workout_butt_x = rhand_x > workout_butt_pos_x and rhand_x < (workout_butt_pos_x + workout_butt_width)
                rhand_y_in_workout_butt_y = rhand_y > workout_butt_pos_y and rhand_y < (workout_butt_pos_y + workout_butt_height)
                rhand_in_workout_butt = rhand_x_in_workout_butt_x and rhand_y_in_workout_butt_y

                if (lhand_in_workout_butt or rhand_in_workout_butt) and not (lhand_in_yoga_butt or rhand_in_yoga_butt):
                    cv2.rectangle(img, 
                                (workout_butt_pos_x, workout_butt_pos_y), 
                                (workout_butt_pos_x + workout_butt_width, workout_butt_pos_y + workout_butt_height), 
                                green_clr, 
                                3)

                    # Detect 'tap' on workout_butt
                    hand_in_workout_butt_curr_time = int(time.time() - hand_in_workout_butt_inittime)
                    if hand_in_workout_butt_curr_time >= 1 and not workout_butt_pressed:
                        
                        # Reset to yoga
                        hand_in_wtimer_inittime = 1000000000000
                        hand_in_ptimer_inittime = 1000000000000

                        label_next_pose = 'T Pose'

                        wtimer_left = trng_duration
                        wtimer_text_size = 2
                        wtimer_curr_rec_width = 0
                        winit_time = time.time()
                        prev_wcurr_time = 0
                        wmins, wsecs = divmod(wtimer_left, 60)
                        wtimer = '{:02d}:{:02d}'.format(wmins, wsecs)

                        ptimer_left = pose_duration
                        ptimer_curr_rec_width = 0
                        pinit_time = time.time()
                        prev_pcurr_time = 0

                        wtimer_tapped = False
                        wtimer_active = True
                        wtimer_show = True
                        ptimer_active = True
                        ptimer_show = True

                        exit_butt_active = False
                        cont_butt_active = False

                        yoga_butt_active = False
                        workout_butt_active = False

                        yoga_active = True
                        workout_active = False

                        cv2.rectangle(img, 
                                (workout_butt_pos_x, workout_butt_pos_y), 
                                (workout_butt_pos_x + workout_butt_width, workout_butt_pos_y + workout_butt_height), 
                                green_clr, 
                                cv2.FILLED)

                        workout_butt_pressed = True

                else:
                    hand_in_workout_butt_inittime = time.time()
                    workout_butt_pressed = False
    
        

    # else:
    #     img = black_matrix


    # Draw framerate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 500), cv2.FONT_HERSHEY_PLAIN, 5, blue_clr, 5)


    cv2.imshow("AIgym", img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()