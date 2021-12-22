import cv2
import numpy as np
import time
import PoseModule as pm
import os
import Constants as cons

dirname = os.path.dirname(__file__)

cap = cv2.VideoCapture(cons.camera_id)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, cons.window_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cons.window_height)
cv2.namedWindow(cons.name_app, cv2.WINDOW_NORMAL)

enable_segmentation=True

detector = pm.poseDetector(enable_segmentation=enable_segmentation)

prev_time = 0

# Init variables for first pose 
trng_seq = list(detector.poses)
#TODO: Get training duration from json
trng_duration = cons.duration_trng
pose_name = trng_seq.pop(0)
pose_duration = detector.poses[pose_name]['duration']
pose_angles = detector.poses[pose_name]['start']['angles']

is_corr_pose = False
label_next_pose = pose_name.capitalize() + cons.lbl_pose

wtimer_left = trng_duration
wtimer_text_size = cons.fnt_size_timer
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

some_bttn_active = False

# Background video 
bg_video_name = os.path.join(dirname, 'pose_1' + cons.format_video)
capBackground = cv2.VideoCapture(bg_video_name)
capBackground.set(cv2.CAP_PROP_FRAME_WIDTH, cons.window_height)
capBackground.set(cv2.CAP_PROP_FRAME_HEIGHT, cons.window_width)


while cap.isOpened():
    _, img = cap.read()

    # Flip the frame horizontally for natural (selfie-view) visualization.
    img = cv2.flip(img, cons.flip_hor)

    lmks, segmentation_mask = detector.analyze(img)

    if lmks:
        
        # Hands Menu Control
        lhand_x, lhand_y, _ = lmks[cons.RIGHT_INDEX]
        rhand_x, rhand_y, _ = lmks[cons.LEFT_INDEX]


        # Youga
        if yoga_active:



            # TODO: Try to use async
            # Segmentation
            if enable_segmentation:
                # Read background video frame
                success, img_back = capBackground.read()
                # Repeat video if it's end
                if not success:
                    capBackground.set(cv2.CAP_PROP_POS_FRAMES, 0)
                else:
                    # TODO: Use video with correct resolution
                    # Resize video frame to be equal window's size
                    img_back = cv2.resize(img_back,(cons.window_width, cons.window_height),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
                    # Add background frame to segmented user's frame
                    condition = np.stack((segmentation_mask,) * 3, axis=-1) > 0.1
                    bg_image = np.zeros(img.shape, dtype=np.uint8)
                    bg_image[:] = img_back
                    img = np.where(condition, img, bg_image)


            # Detect if pose is correct
            is_corr_pose = detector.correct_pose(img, lmks, pose_angles, draw=True)

            # Update the color (to green) with which the label will be written on the image.
            label_clr = cons.clr_green if is_corr_pose or label_next_pose == cons.lbl_done else cons.clr_red

            # Write the pose label on the output image. 
            cv2.putText(img, label_next_pose, (400, 75), cv2.FONT_HERSHEY_DUPLEX, cons.fnt_size_menu, label_clr, cons.fnt_thick)
            


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
                    wtimer= cons.lbl_time_end
                    wtimer_text_size -= 1
                    winit_time = time.time()
            else:
                winit_time = time.time()

            if wtimer_show:
                #Draw workout timer
                cv2.rectangle(img, 
                            (wtimer_pos_x, wtimer_pos_y), 
                            (wtimer_pos_x + wtimer_width, wtimer_pos_y + wtimer_height), 
                            cons.clr_black, 
                            cons.fnt_thick)

                if wtimer_left > 0:
                    cv2.rectangle(img, 
                                (wtimer_pos_x, wtimer_pos_y), 
                                (wtimer_pos_x + wtimer_curr_rec_width, wtimer_pos_y + wtimer_height), 
                                cons.clr_black, 
                                cv2.FILLED)
                else:
                    cv2.rectangle(img, 
                                (wtimer_pos_x, wtimer_pos_y), 
                                (wtimer_pos_x + wtimer_width, wtimer_pos_y + wtimer_height), 
                                cons.clr_black, 
                                cv2.FILLED)
                
                #Workout timer text
                cv2.putText(img, 
                            cons.lbl_pause, 
                            (wtimer_pos_x + 5, wtimer_pos_y + 65), 
                            cv2.FONT_HERSHEY_DUPLEX, 
                            cons.fnt_size_menu, 
                            cons.clr_white, 
                            cons.fnt_thick)
                cv2.putText(img, 
                            wtimer, 
                            (wtimer_pos_x + 115, wtimer_pos_y + 65), 
                            cv2.FONT_HERSHEY_DUPLEX, 
                            wtimer_text_size, 
                            cons.clr_white, 
                            cons.fnt_thick)

            
            #Pose timer
            ptimer_pos_y = 10
            ptimer_width = 300
            ptimer_height = 100
            ptimer_pos_x = 650  # window_width - ptimer_width - 10
            ptimer_width_step = ptimer_width / pose_duration
            ptimer_text = cons.lbl_next
            
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
                            label_next_pose = cons.lbl_done
                            ptimer_active = False

                        # Reset pose variables to next pose
                        elif is_corr_pose:
                            is_corr_pose = False
                            
                            # Set next pose
                            pose_name = trng_seq.pop(0)
                            # Set new values to pose variables 
                            label_next_pose = pose_name.capitalize() + cons.lbl_pose
                            pose_duration = detector.poses[pose_name]['duration']
                            pose_angles = detector.poses[pose_name]['start']['angles']
                            

                else:
                    pinit_time = time.time()


            if ptimer_show:
                cv2.rectangle(img, 
                            (ptimer_pos_x, ptimer_pos_y), 
                            (ptimer_pos_x + ptimer_width, ptimer_pos_y + ptimer_height), 
                            cons.clr_black, 
                            cons.fnt_thick)

                if ptimer_left > 0:
                    cv2.rectangle(img, 
                                (ptimer_pos_x, ptimer_pos_y), 
                                (ptimer_pos_x + ptimer_curr_rec_width, ptimer_pos_y + ptimer_height), 
                                cons.clr_black, 
                                cv2.FILLED)
                else:
                    cv2.rectangle(img, 
                                (ptimer_pos_x, ptimer_pos_y), 
                                (ptimer_pos_x + ptimer_width, ptimer_pos_y + ptimer_height), 
                                cons.clr_black, 
                                cv2.FILLED)
                
                #Workout timer text
                cv2.putText(img, 
                            ptimer_text, 
                            (ptimer_pos_x + 100, ptimer_pos_y + 65), 
                            cv2.FONT_HERSHEY_DUPLEX, 
                            cons.fnt_size_menu, 
                            cons.clr_white, 
                            cons.fnt_thick)
            
            
            # Wtimer
            if wtimer_active:
                lhand_x_in_wtimer_x = lhand_x > wtimer_pos_x and lhand_x < (wtimer_pos_x + wtimer_width)
                lhand_y_in_wtimer_y = lhand_y > wtimer_pos_y and lhand_y < (wtimer_pos_y + wtimer_height)
                lhand_in_wtimer = lhand_x_in_wtimer_x and lhand_y_in_wtimer_y

                rhand_x_in_wtimer_x = rhand_x > wtimer_pos_x and rhand_x < (wtimer_pos_x + wtimer_width)
                rhand_y_in_wtimer_y = rhand_y > wtimer_pos_y and rhand_y < (wtimer_pos_y + wtimer_height)
                rhand_in_wtimer = rhand_x_in_wtimer_x and rhand_y_in_wtimer_y

                # Detect if hand in button area
                if (lhand_in_wtimer or rhand_in_wtimer) and not some_bttn_active:
                    cv2.rectangle(img, 
                                (wtimer_pos_x, wtimer_pos_y), 
                                (wtimer_pos_x + wtimer_width, wtimer_pos_y + wtimer_height), 
                                cons.clr_green, 
                                cons.fnt_thick)
                                
                    # Detect 'tap' on wtimer
                    hand_in_wtimer_curr_time = int(time.time() - hand_in_wtimer_inittime)
                    if hand_in_wtimer_curr_time >= cons.time_tap and not wtimer_pressed:
                        # Turn off other buttons
                        some_bttn_active = True

                        wtimer_tapped = True
                        exit_butt_active = True
                        cont_butt_active = True
                        
                        cv2.rectangle(img, 
                                (wtimer_pos_x, wtimer_pos_y), 
                                (wtimer_pos_x + wtimer_width, wtimer_pos_y + wtimer_height), 
                                cons.clr_green, 
                                cv2.FILLED)

                        wtimer_pressed = True
                else:
                    hand_in_wtimer_inittime = time.time()
                    wtimer_pressed = False
                    # Turn on other buttons
                    some_bttn_active = False

            # Draw pause buttons
            if wtimer_tapped:
                
                # Deactivate wtimer and ptimer buttons
                wtimer_active = False
                ptimer_active = False

                # Exit button
                if exit_butt_active:
                    
                    # Draw exit button
                    exit_butt_pos_x = int(cons.window_width / 5.5)
                    exit_butt_pos_y = 200
                    exit_butt_width = 300
                    exit_butt_height = 100

                    cv2.rectangle(img, 
                                (exit_butt_pos_x, exit_butt_pos_y), 
                                (exit_butt_pos_x + exit_butt_width, exit_butt_pos_y + exit_butt_height), 
                                cons.clr_black, 
                                cons.fnt_thick)
                    cv2.rectangle(img, 
                                (exit_butt_pos_x, exit_butt_pos_y), 
                                (exit_butt_pos_x + exit_butt_width, exit_butt_pos_y + exit_butt_height), 
                                cons.clr_black, 
                                cv2.FILLED)
                    
                    # Exit button text
                    cv2.putText(img, 
                                cons.lbl_exit, 
                                (exit_butt_pos_x + 100, exit_butt_pos_y + 65), 
                                cv2.FONT_HERSHEY_DUPLEX, 
                                cons.fnt_size_menu, 
                                cons.clr_white, 
                                cons.fnt_thick)

                    lhand_x_in_exit_butt_x = lhand_x > exit_butt_pos_x and lhand_x < (exit_butt_pos_x + exit_butt_width)
                    lhand_y_in_exit_butt_y = lhand_y > exit_butt_pos_y and lhand_y < (exit_butt_pos_y + exit_butt_height)
                    lhand_in_exit_butt = lhand_x_in_exit_butt_x and lhand_y_in_exit_butt_y

                    rhand_x_in_exit_butt_x = rhand_x > exit_butt_pos_x and rhand_x < (exit_butt_pos_x + exit_butt_width)
                    rhand_y_in_exit_butt_y = rhand_y > exit_butt_pos_y and rhand_y < (exit_butt_pos_y + exit_butt_height)
                    rhand_in_exit_butt = rhand_x_in_exit_butt_x and rhand_y_in_exit_butt_y

                    if (lhand_in_exit_butt or rhand_in_exit_butt) and not some_bttn_active:
                        cv2.rectangle(img, 
                                    (exit_butt_pos_x, exit_butt_pos_y), 
                                    (exit_butt_pos_x + exit_butt_width, exit_butt_pos_y + exit_butt_height), 
                                    cons.clr_green, 
                                    cons.fnt_thick)
                        
                        # Detect 'tap' on exit_butt
                        hand_in_exit_butt_curr_time = int(time.time() - hand_in_exit_butt_inittime)
                        if hand_in_exit_butt_curr_time >= cons.time_tap and not exit_butt_pressed:
                             # Turn off other buttons
                            some_bttn_active = True

                            cv2.rectangle(img, 
                                    (exit_butt_pos_x, exit_butt_pos_y), 
                                    (exit_butt_pos_x + exit_butt_width, exit_butt_pos_y + exit_butt_height), 
                                    cons.clr_green, 
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
                        # Turn on other buttons
                        some_bttn_active = False
                
                

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
                                cons.clr_black, 
                                cons.fnt_thick)
                    cv2.rectangle(img, 
                                (cont_butt_pos_x, cont_butt_pos_y), 
                                (cont_butt_pos_x + cont_butt_width, cont_butt_pos_y + cont_butt_height), 
                                cons.clr_black, 
                                cv2.FILLED)
                    
                    # Exit button text
                    cv2.putText(img, cons.lbl_continue, (cont_butt_pos_x + 80, cont_butt_pos_y + 65), cv2.FONT_HERSHEY_DUPLEX, cons.fnt_size_menu, 
                                cons.clr_white, cons.fnt_thick)

                    lhand_x_in_cont_butt_x = lhand_x > cont_butt_pos_x and lhand_x < (cont_butt_pos_x + cont_butt_width)
                    lhand_y_in_cont_butt_y = lhand_y > cont_butt_pos_y and lhand_y < (cont_butt_pos_y + cont_butt_height)
                    lhand_in_cont_butt = lhand_x_in_cont_butt_x and lhand_y_in_cont_butt_y

                    rhand_x_in_cont_butt_x = rhand_x > cont_butt_pos_x and rhand_x < (cont_butt_pos_x + cont_butt_width)
                    rhand_y_in_cont_butt_y = rhand_y > cont_butt_pos_y and rhand_y < (cont_butt_pos_y + cont_butt_height)
                    rhand_in_cont_butt = rhand_x_in_cont_butt_x and rhand_y_in_cont_butt_y

                    if (lhand_in_cont_butt or rhand_in_cont_butt) and not some_bttn_active:
                        cv2.rectangle(img, 
                                    (cont_butt_pos_x, cont_butt_pos_y), 
                                    (cont_butt_pos_x + cont_butt_width, cont_butt_pos_y + cont_butt_height), 
                                    cons.clr_green, 
                                    cons.fnt_thick)

                        # Detect 'tap' on cont_butt
                        hand_in_cont_butt_curr_time = int(time.time() - hand_in_cont_butt_inittime)
                        if hand_in_cont_butt_curr_time >= cons.time_tap and not cont_butt_pressed:
                            # Turn off other buttons
                            some_bttn_active = True

                            cont_butt_active = False
                            wtimer_tapped = False
                            wtimer_active = True
                            ptimer_active = True

                            cv2.rectangle(img, 
                                    (cont_butt_pos_x, cont_butt_pos_y), 
                                    (cont_butt_pos_x + cont_butt_width, cont_butt_pos_y + cont_butt_height), 
                                    cons.clr_green, 
                                    cv2.FILLED)

                            cont_butt_pressed = True

                    else:
                        hand_in_cont_butt_inittime = time.time()
                        cont_butt_pressed = False
                        # Turn on other buttons
                        some_bttn_active = False


            # Ptimer
            if ptimer_active:
                lhand_x_in_ptimer_x = lhand_x > ptimer_pos_x and lhand_x < (ptimer_pos_x + ptimer_width)
                lhand_y_in_ptimer_y = lhand_y > ptimer_pos_y and lhand_y < (ptimer_pos_y + ptimer_height)
                lhand_in_ptimer = lhand_x_in_ptimer_x and lhand_y_in_ptimer_y

                rhand_x_in_ptimer_x = rhand_x > ptimer_pos_x and rhand_x < (ptimer_pos_x + ptimer_width)
                rhand_y_in_ptimer_y = rhand_y > ptimer_pos_y and rhand_y < (ptimer_pos_y + ptimer_height)
                rhand_in_ptimer = rhand_x_in_ptimer_x and rhand_y_in_ptimer_y
                # Detect if hand in button area
                if (lhand_in_ptimer or rhand_in_ptimer) and not some_bttn_active:
                    cv2.rectangle(img, 
                                (ptimer_pos_x, ptimer_pos_y), 
                                (ptimer_pos_x + ptimer_width, ptimer_pos_y + ptimer_height), 
                                cons.clr_green, 
                                cons.fnt_thick)

                    # Detect 'tap' on ptimer
                    hand_in_ptimer_curr_time = int(time.time() - hand_in_ptimer_inittime)
                    if hand_in_ptimer_curr_time >= cons.time_tap and not ptimer_pressed:
                        # Turn off other buttons
                        some_bttn_active = True

                        ptimer_left = pose_duration
                        ptimer_curr_rec_width = 0
                        
                        #TODO: DRY
                        # Check if user is done training
                        if not trng_seq:
                            label_next_pose = cons.lbl_done
                            ptimer_active = False

                            some_bttn_active = False

                        # Reset pose variables to next pose
                        else:

                            # Set next pose
                            pose_name = trng_seq.pop(0)
                            # Set new values to pose variables 
                            label_next_pose = pose_name.capitalize() + cons.lbl_pose
                            pose_duration = detector.poses[pose_name]['duration']
                            pose_angles = detector.poses[pose_name]['start']['angles']


                        cv2.rectangle(img, 
                                (ptimer_pos_x, ptimer_pos_y), 
                                (ptimer_pos_x + ptimer_width, ptimer_pos_y + ptimer_height), 
                                cons.clr_green, 
                                cv2.FILLED)

                        ptimer_pressed = True

                else:
                    hand_in_ptimer_inittime = time.time()
                    ptimer_pressed = False
                    # Turn on other buttons
                    some_bttn_active = False


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
                        cons.clr_black, 
                        cons.fnt_thick)
            cv2.rectangle(img, 
                        (yoga_butt_pos_x, yoga_butt_pos_y), 
                        (yoga_butt_pos_x + yoga_butt_width, yoga_butt_pos_y + yoga_butt_height), 
                        cons.clr_black, 
                        cv2.FILLED)
            
            # yoga button text
            cv2.putText(img, 
                        cons.lbl_yoga, 
                        (yoga_butt_pos_x + 100, yoga_butt_pos_y + 65), 
                        cv2.FONT_HERSHEY_DUPLEX, 
                        cons.fnt_size_menu, 
                        cons.clr_white, 
                        cons.fnt_thick)

            # Tap yoga button
            if yoga_butt_active:
                lhand_x_in_yoga_butt_x = lhand_x > yoga_butt_pos_x and lhand_x < (yoga_butt_pos_x + yoga_butt_width)
                lhand_y_in_yoga_butt_y = lhand_y > yoga_butt_pos_y and lhand_y < (yoga_butt_pos_y + yoga_butt_height)
                lhand_in_yoga_butt = lhand_x_in_yoga_butt_x and lhand_y_in_yoga_butt_y

                rhand_x_in_yoga_butt_x = rhand_x > yoga_butt_pos_x and rhand_x < (yoga_butt_pos_x + yoga_butt_width)
                rhand_y_in_yoga_butt_y = rhand_y > yoga_butt_pos_y and rhand_y < (yoga_butt_pos_y + yoga_butt_height)
                rhand_in_yoga_butt = rhand_x_in_yoga_butt_x and rhand_y_in_yoga_butt_y

                if (lhand_in_yoga_butt or rhand_in_yoga_butt) and not some_bttn_active:
                    cv2.rectangle(img, 
                                (yoga_butt_pos_x, yoga_butt_pos_y), 
                                (yoga_butt_pos_x + yoga_butt_width, yoga_butt_pos_y + yoga_butt_height), 
                                cons.clr_green, 
                                cons.fnt_thick)

                    # Detect 'tap' on yoga_butt
                    hand_in_yoga_butt_curr_time = int(time.time() - hand_in_yoga_butt_inittime)
                    if hand_in_yoga_butt_curr_time >= cons.time_tap and not yoga_butt_pressed:
                        # Turn off other buttons
                        some_bttn_active = True

                        # Reset to yoga
                        hand_in_wtimer_inittime = cons.num_big
                        hand_in_ptimer_inittime = cons.num_big

                        # Init variables for first pose 
                        trng_seq = list(detector.poses)
                        #TODO: Get training duration from json
                        trng_duration = cons.duration_trng
                        pose_name = trng_seq.pop(0)
                        pose_duration = detector.poses[pose_name]['duration']
                        pose_angles = detector.poses[pose_name]['start']['angles']

                        label_next_pose = pose_name.capitalize() + cons.lbl_pose

                        wtimer_left = trng_duration
                        wtimer_text_size = cons.fnt_size_timer
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

                        some_bttn_active = False

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
                                cons.clr_green, 
                                cv2.FILLED)

                else:
                    hand_in_yoga_butt_inittime = time.time()
                    yoga_butt_pressed = False
                    # Turn on other buttons
                    some_bttn_active = False

        if workout_butt_active:
            # Draw workout button
            workout_butt_pos_x = 650 # yoga_butt_pos_x + yoga_butt_width + 40
            workout_butt_pos_y = 10
            workout_butt_width = 300
            workout_butt_height = 100

            cv2.rectangle(img, 
                        (workout_butt_pos_x, workout_butt_pos_y), 
                        (workout_butt_pos_x + workout_butt_width, workout_butt_pos_y + workout_butt_height), 
                        cons.clr_black, 
                        cons.fnt_thick)
            cv2.rectangle(img, 
                        (workout_butt_pos_x, workout_butt_pos_y), 
                        (workout_butt_pos_x + workout_butt_width, workout_butt_pos_y + workout_butt_height), 
                        cons.clr_black, 
                        cv2.FILLED)
            
            # workout button text
            cv2.putText(img, 
                        cons.lbl_workout,
                        (workout_butt_pos_x + 100, workout_butt_pos_y + 65), 
                        cv2.FONT_HERSHEY_DUPLEX, 
                        cons.fnt_size_menu, 
                        cons.clr_white, 
                        cons.fnt_thick)

            # Tap workout button
            if workout_butt_active:
                lhand_x_in_workout_butt_x = lhand_x > workout_butt_pos_x and lhand_x < (workout_butt_pos_x + workout_butt_width)
                lhand_y_in_workout_butt_y = lhand_y > workout_butt_pos_y and lhand_y < (workout_butt_pos_y + workout_butt_height)
                lhand_in_workout_butt = lhand_x_in_workout_butt_x and lhand_y_in_workout_butt_y

                rhand_x_in_workout_butt_x = rhand_x > workout_butt_pos_x and rhand_x < (workout_butt_pos_x + workout_butt_width)
                rhand_y_in_workout_butt_y = rhand_y > workout_butt_pos_y and rhand_y < (workout_butt_pos_y + workout_butt_height)
                rhand_in_workout_butt = rhand_x_in_workout_butt_x and rhand_y_in_workout_butt_y

                if (lhand_in_workout_butt or rhand_in_workout_butt) and not some_bttn_active:
                    cv2.rectangle(img, 
                                (workout_butt_pos_x, workout_butt_pos_y), 
                                (workout_butt_pos_x + workout_butt_width, workout_butt_pos_y + workout_butt_height), 
                                cons.clr_green, 
                                cons.fnt_thick)

                    # Detect 'tap' on workout_butt
                    hand_in_workout_butt_curr_time = int(time.time() - hand_in_workout_butt_inittime)
                    if hand_in_workout_butt_curr_time >= cons.time_tap and not workout_butt_pressed:
                        # Turn off other buttons
                        some_bttn_active = True
                        
                        # Reset to yoga
                        hand_in_wtimer_inittime = cons.num_big
                        hand_in_ptimer_inittime = cons.num_big

                        # Init variables for first pose 
                        trng_seq = list(detector.poses)
                        #TODO: Get training duration from json
                        trng_duration = cons.duration_trng
                        pose_name = trng_seq.pop(0)
                        pose_duration = detector.poses[pose_name]['duration']
                        pose_angles = detector.poses[pose_name]['start']['angles']

                        label_next_pose = pose_name.capitalize() + cons.lbl_pose

                        wtimer_left = trng_duration
                        wtimer_text_size = cons.fnt_size_timer
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

                        some_bttn_active = False

                        exit_butt_active = False
                        cont_butt_active = False

                        yoga_butt_active = False
                        workout_butt_active = False

                        yoga_active = True
                        workout_active = False

                        cv2.rectangle(img, 
                                (workout_butt_pos_x, workout_butt_pos_y), 
                                (workout_butt_pos_x + workout_butt_width, workout_butt_pos_y + workout_butt_height), 
                                cons.clr_green, 
                                cv2.FILLED)

                        workout_butt_pressed = True

                else:
                    hand_in_workout_butt_inittime = time.time()
                    workout_butt_pressed = False
                    # Turn on other buttons
                    some_bttn_active = False
    

    # Draw framerate
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time
    cv2.putText(img, str(int(fps)), (50, 500), cv2.FONT_HERSHEY_DUPLEX, cons.fnt_size_menu, cons.clr_blue, cons.fnt_thick)


    cv2.imshow(cons.name_app, img)

    if cv2.waitKey(cons.time_wait_close_window) & 0xFF == ord(cons.kbrd_quit):
        break

cap.release()
cv2.destroyAllWindows()