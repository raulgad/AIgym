import cv2
import numpy as np
import time
import PoseModule as pm
import os
import Constants as cons

dirname = os.path.dirname(__file__)

# Video from camera
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
pose_name = trng_seq.pop(0)
pose_duration = detector.poses[pose_name]['duration']
pose_angles = detector.poses[pose_name]['start']['angles']

is_corr_pose = False

label_next_pose = pose_name.capitalize() + cons.lbl_pose

trng_time_left = cons.duration_trng
prev_trng_curr_time = 0
trng_init_time = time.time()
trng_curr_time = 0
trng_mins, trng_secs = divmod(trng_time_left, 60)

pause_bttn_lbl = '{:02d}:{:02d}'.format(trng_mins, trng_secs)
pause_bttn_text_size = cons.fnt_size_timer
pause_bttn_curr_rec_width = 0

next_bttn_curr_rec_width = 0
pose_time_left = pose_duration
prev_pose_curr_time = 0
pose_init_time = time.time()
pose_curr_time = 0

pause_bttn_active = True
next_bttn_active = True

pause_bttn_show = True
next_bttn_show = True

exit_butt_active = False
cont_butt_active = False

yoga_butt_active = True
workout_butt_active = True

yoga_active = False
workout_active = False

hand_in_pause_bttn_inittime = time.time()
hand_in_pause_bttn_curr_time = 0

hand_in_exit_butt_inittime = time.time()
hand_in_exit_butt_curr_time = 0

hand_in_cont_butt_inittime = time.time()
hand_in_cont_butt_curr_time = 0

hand_in_next_bttn_inittime = time.time()
hand_in_next_bttn_curr_time = 0

hand_in_yoga_butt_inittime = time.time()
hand_in_yoga_butt_curr_time = 0

hand_in_workout_butt_inittime = time.time()
hand_in_workout_butt_curr_time = 0


lhand_in_pause_bttn = False
rhand_in_pause_bttn = False

lhand_in_next_bttn = False
rhand_in_next_bttn = False
lhand_in_exit_butt = False
rhand_in_exit_butt = False
lhand_in_cont_butt = False
rhand_in_cont_butt = False
lhand_in_yoga_butt = False
rhand_in_yoga_butt = False
lhand_in_workout_butt = False
rhand_in_workout_butt = False

next_bttn_tapped = False
pause_bttn_tapped = False
exit_butt_tapped = False
cont_butt_tapped = False
yoga_butt_tapped = False
workout_butt_tapped = False

show_paused_bttns = False
some_bttn_active = False

# Background video 
bg_video_name = os.path.join(dirname, 'pose_1' + cons.format_video)
cap_backgrd = cv2.VideoCapture(bg_video_name)
cap_backgrd.set(cv2.CAP_PROP_FRAME_WIDTH, cons.window_height)
cap_backgrd.set(cv2.CAP_PROP_FRAME_HEIGHT, cons.window_width)

cap_backgrd_paused = False
paused_img_back = []

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
                success, img_back = cap_backgrd.read()
                # Set paused background image if user tap on Pause button
                if cap_backgrd_paused: img_back = paused_img_back
                # Repeat video if it's end
                if not success:
                    cap_backgrd.set(cv2.CAP_PROP_POS_FRAMES, 0)
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

            # Set label color and text
            label_clr = cons.clr_green if is_corr_pose or label_next_pose == cons.lbl_done else cons.clr_red
            label_next_pose = (pose_name.capitalize() + cons.lbl_pose) if is_corr_pose else cons.lbl_correct_limbs

            # Write the pose label on the output image. 
            cv2.putText(img, label_next_pose, (400, 75), cv2.FONT_HERSHEY_DUPLEX, cons.fnt_size_menu, label_clr, cons.fnt_thick)
            


            # Workout timer

            pause_bttn_pos_x = 10
            pause_bttn_pos_y = 10
            pause_bttn_width = 300
            pause_bttn_height = 100
            pause_bttn_width_step = pause_bttn_width / cons.duration_trng

            # Change training time button if it active
            if pause_bttn_active:
                
                if trng_time_left > 0:
                    trng_curr_time = int(time.time() - trng_init_time)

                    if prev_trng_curr_time != trng_curr_time:
                        pause_bttn_curr_rec_width += int(pause_bttn_width_step)
                        prev_trng_curr_time = trng_curr_time
                        trng_time_left -= 1

                        trng_mins, trng_secs = divmod(trng_time_left, 60)
                        pause_bttn_lbl = '{:02d}:{:02d}'.format(trng_mins, trng_secs)
                else:
                    pause_bttn_lbl= cons.lbl_time_end
                    pause_bttn_text_size -= 1
                    trng_init_time = time.time()
            else:
                trng_init_time = time.time()

            if pause_bttn_show:
                #Draw workout timer
                cv2.rectangle(img, 
                            (pause_bttn_pos_x, pause_bttn_pos_y), 
                            (pause_bttn_pos_x + pause_bttn_width, pause_bttn_pos_y + pause_bttn_height), 
                            cons.clr_black, 
                            cons.fnt_thick)
                cv2.rectangle(img, 
                            (pause_bttn_pos_x, pause_bttn_pos_y), 
                            (pause_bttn_pos_x + pause_bttn_width, pause_bttn_pos_y + pause_bttn_height), 
                            cons.clr_gray, 
                            cv2.FILLED)

                if trng_time_left > 0:
                    cv2.rectangle(img, 
                                (pause_bttn_pos_x, pause_bttn_pos_y), 
                                (pause_bttn_pos_x + pause_bttn_curr_rec_width, pause_bttn_pos_y + pause_bttn_height), 
                                cons.clr_black, 
                                cv2.FILLED)
                else:
                    cv2.rectangle(img, 
                                (pause_bttn_pos_x, pause_bttn_pos_y), 
                                (pause_bttn_pos_x + pause_bttn_width, pause_bttn_pos_y + pause_bttn_height), 
                                cons.clr_black, 
                                cv2.FILLED)
                
                #Workout timer text
                cv2.putText(img, 
                            cons.lbl_pause, 
                            (pause_bttn_pos_x + 5, pause_bttn_pos_y + 65), 
                            cv2.FONT_HERSHEY_DUPLEX, 
                            cons.fnt_size_menu, 
                            cons.clr_white, 
                            cons.fnt_thick)
                cv2.putText(img, 
                            pause_bttn_lbl, 
                            (pause_bttn_pos_x + 115, pause_bttn_pos_y + 65), 
                            cv2.FONT_HERSHEY_DUPLEX, 
                            pause_bttn_text_size, 
                            cons.clr_white, 
                            cons.fnt_thick)

            
            #Pose timer
            next_bttn_pos_y = 10
            next_bttn_width = 300
            next_bttn_height = 100
            next_bttn_pos_x = 650  # window_width - next_bttn_width - 10
            next_bttn_width_step = next_bttn_width / pose_duration
            # Change pose timer button if it active
            if next_bttn_active:
                # Change anything only if we detect any pose
                if is_corr_pose:
                    # Fill pose timer button by increasing filled button's rectangle each time when
                    # we current pose is equal label_next_pose and when pose timer is not end.
                    if pose_time_left > 0 and is_corr_pose:
                        # Calculate time that starts right after we detect correct pose (label == label_next_pose)
                        pose_curr_time = int(time.time() - pose_init_time)
                        # Change filled pose timer rectangle each second. One second is 
                        # passed when 'prev_pose_curr_time != pose_curr_time'
                        if prev_pose_curr_time != pose_curr_time:
                            # Increase filled pose timer rectangle for one time (+ next_bttn_curr_rec_width)
                            next_bttn_curr_rec_width += int(next_bttn_width_step)
                            # Save current pose time (pose_curr_time) to prev_pose_curr_time for detect 
                            #  when 1 second is passed
                            prev_pose_curr_time = pose_curr_time
                            # Update timer that indicates how much time is left to end the pose.
                            pose_time_left -= 1
                    
                    elif pose_time_left <= 0:
                        # Reset timers and pose label if pose time is ended.
                        pose_time_left = pose_duration
                        next_bttn_curr_rec_width = 0

                        # pose_contr.update_pose(
                        #     # Check if user is done training
                        #     if not trng_seq:
                        #         label_next_pose = cons.lbl_done
                        #         timing.next_bttn_active = False
                        #         menu.some_bttn_active = False
                        #     # Reset pose variables to next pose
                        #     elif is_corr_pose:
                        #         is_corr_pose = False
                        #         # Set next pose
                        #         pose_name = trng_seq.pop(0)
                        #         # Set new values to pose variables 
                        #         label_next_pose = pose_name.capitalize() + cons.lbl_pose
                        #         pose_duration = detector.poses[pose_name]['duration']
                        #         pose_angles = detector.poses[pose_name]['start']['angles']
                        # )

                        # Check if user is done training
                        if not trng_seq:
                            label_next_pose = cons.lbl_done
                            next_bttn_active = False
                            some_bttn_active = False
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
                    pose_init_time = time.time()


            if next_bttn_show:
                cv2.rectangle(img, 
                                (next_bttn_pos_x, next_bttn_pos_y), 
                                (next_bttn_pos_x + next_bttn_width, next_bttn_pos_y + next_bttn_height), 
                                cons.clr_black, 
                                cons.fnt_thick)
                cv2.rectangle(img, 
                                (next_bttn_pos_x, next_bttn_pos_y), 
                                (next_bttn_pos_x + next_bttn_width, next_bttn_pos_y + next_bttn_height), 
                                cons.clr_gray, 
                                cv2.FILLED)
                
                if pose_time_left > 0:
                    cv2.rectangle(img, 
                                (next_bttn_pos_x, next_bttn_pos_y), 
                                (next_bttn_pos_x + next_bttn_curr_rec_width, next_bttn_pos_y + next_bttn_height), 
                                cons.clr_black, 
                                cv2.FILLED)
                else:
                    cv2.rectangle(img, 
                                (next_bttn_pos_x, next_bttn_pos_y), 
                                (next_bttn_pos_x + next_bttn_width, next_bttn_pos_y + next_bttn_height), 
                                cons.clr_black, 
                                cv2.FILLED)
               
                # Pose timer text
                cv2.putText(img, 
                            cons.lbl_next, 
                            (next_bttn_pos_x + 100, next_bttn_pos_y + 65), 
                            cv2.FONT_HERSHEY_DUPLEX, 
                            cons.fnt_size_menu, 
                            cons.clr_white, 
                            cons.fnt_thick)
            
            
            # Pause button
            if pause_bttn_active:
                lhand_x_in_pause_bttn_x = lhand_x > pause_bttn_pos_x and lhand_x < (pause_bttn_pos_x + pause_bttn_width)
                lhand_y_in_pause_bttn_y = lhand_y > pause_bttn_pos_y and lhand_y < (pause_bttn_pos_y + pause_bttn_height)
                lhand_in_pause_bttn = lhand_x_in_pause_bttn_x and lhand_y_in_pause_bttn_y

                rhand_x_in_pause_bttn_x = rhand_x > pause_bttn_pos_x and rhand_x < (pause_bttn_pos_x + pause_bttn_width)
                rhand_y_in_pause_bttn_y = rhand_y > pause_bttn_pos_y and rhand_y < (pause_bttn_pos_y + pause_bttn_height)
                rhand_in_pause_bttn = rhand_x_in_pause_bttn_x and rhand_y_in_pause_bttn_y

                # Detect if hand in button area
                if (lhand_in_pause_bttn or rhand_in_pause_bttn) and not some_bttn_active:
                    cv2.rectangle(img, 
                                (pause_bttn_pos_x, pause_bttn_pos_y), 
                                (pause_bttn_pos_x + pause_bttn_width, pause_bttn_pos_y + pause_bttn_height), 
                                cons.clr_green, 
                                cons.fnt_thick)
                                
                    # Detect 'tap' on pause_bttn
                    hand_in_pause_bttn_curr_time = int(time.time() - hand_in_pause_bttn_inittime)
                    if hand_in_pause_bttn_curr_time >= cons.time_tap and not pause_bttn_tapped:
                        # Turn off other buttons
                        some_bttn_active = True

                        show_paused_bttns = True
                        exit_butt_active = True
                        cont_butt_active = True

                        # Pause video
                        cap_backgrd_paused = True
                        paused_img_back = img_back

                        cv2.rectangle(img, 
                                (pause_bttn_pos_x, pause_bttn_pos_y), 
                                (pause_bttn_pos_x + pause_bttn_width, pause_bttn_pos_y + pause_bttn_height), 
                                cons.clr_green, 
                                cv2.FILLED)

                        pause_bttn_tapped = True
                else:
                    hand_in_pause_bttn_inittime = time.time()
                    pause_bttn_tapped = False
                    # Turn on other buttons
                    some_bttn_active = False

            # Draw pause buttons
            if show_paused_bttns:
                
                # Deactivate pause_bttn and next_bttn buttons
                pause_bttn_active = False
                next_bttn_active = False

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
                        if hand_in_exit_butt_curr_time >= cons.time_tap and not exit_butt_tapped:
                             # Turn off other buttons
                            some_bttn_active = True

                            cv2.rectangle(img, 
                                    (exit_butt_pos_x, exit_butt_pos_y), 
                                    (exit_butt_pos_x + exit_butt_width, exit_butt_pos_y + exit_butt_height), 
                                    cons.clr_green, 
                                    cv2.FILLED)
                            
                            exit_butt_active = False
                            show_paused_bttns = False
                            yoga_active = False
                            yoga_butt_active = True
                            workout_butt_active = True

                            exit_butt_tapped = True

                    else:
                        hand_in_exit_butt_inittime = time.time()
                        exit_butt_tapped = False
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
                        if hand_in_cont_butt_curr_time >= cons.time_tap and not cont_butt_tapped:
                            # Turn off other buttons
                            some_bttn_active = True

                            cont_butt_active = False
                            show_paused_bttns = False
                            pause_bttn_active = True
                            next_bttn_active = True
                            cap_backgrd_paused = False

                            cv2.rectangle(img, 
                                    (cont_butt_pos_x, cont_butt_pos_y), 
                                    (cont_butt_pos_x + cont_butt_width, cont_butt_pos_y + cont_butt_height), 
                                    cons.clr_green, 
                                    cv2.FILLED)

                            cont_butt_tapped = True

                    else:
                        hand_in_cont_butt_inittime = time.time()
                        cont_butt_tapped = False
                        # Turn on other buttons
                        some_bttn_active = False


            # next_bttn
            if next_bttn_active:
                lhand_x_in_next_bttn_x = lhand_x > next_bttn_pos_x and lhand_x < (next_bttn_pos_x + next_bttn_width)
                lhand_y_in_next_bttn_y = lhand_y > next_bttn_pos_y and lhand_y < (next_bttn_pos_y + next_bttn_height)
                lhand_in_next_bttn = lhand_x_in_next_bttn_x and lhand_y_in_next_bttn_y

                rhand_x_in_next_bttn_x = rhand_x > next_bttn_pos_x and rhand_x < (next_bttn_pos_x + next_bttn_width)
                rhand_y_in_next_bttn_y = rhand_y > next_bttn_pos_y and rhand_y < (next_bttn_pos_y + next_bttn_height)
                rhand_in_next_bttn = rhand_x_in_next_bttn_x and rhand_y_in_next_bttn_y
                # Detect if hand in button area
                if (lhand_in_next_bttn or rhand_in_next_bttn) and not some_bttn_active:
                    cv2.rectangle(img, 
                                (next_bttn_pos_x, next_bttn_pos_y), 
                                (next_bttn_pos_x + next_bttn_width, next_bttn_pos_y + next_bttn_height), 
                                cons.clr_green, 
                                cons.fnt_thick)

                    # Detect 'tap' on next_bttn
                    hand_in_next_bttn_curr_time = int(time.time() - hand_in_next_bttn_inittime)
                    if hand_in_next_bttn_curr_time >= cons.time_tap and not next_bttn_tapped:
                        # Turn off other buttons
                        some_bttn_active = True

                        pose_time_left = pose_duration
                        next_bttn_curr_rec_width = 0

                        # pose_contr.update_pose (
                        #     # Check if user is done training
                        #     if not trng_seq:
                        #         label_next_pose = cons.lbl_done
                        #         timing.next_bttn_active = False
                        #         menu.some_bttn_active = False
                        #     # Reset pose variables to next pose
                        #     elif is_corr_pose:
                        #         is_corr_pose = False
                        #         # Set next pose
                        #         pose_name = trng_seq.pop(0)
                        #         # Set new values to pose variables 
                        #         label_next_pose = pose_name.capitalize() + cons.lbl_pose
                        #         pose_duration = detector.poses[pose_name]['duration']
                        #         pose_angles = detector.poses[pose_name]['start']['angles']
                        # )
                        
                        #TODO: DRY
                        # Check if user is done training
                        if not trng_seq:
                            label_next_pose = cons.lbl_done
                            next_bttn_active = False
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
                                (next_bttn_pos_x, next_bttn_pos_y), 
                                (next_bttn_pos_x + next_bttn_width, next_bttn_pos_y + next_bttn_height), 
                                cons.clr_green, 
                                cv2.FILLED)

                        next_bttn_tapped = True

                else:
                    hand_in_next_bttn_inittime = time.time()
                    next_bttn_tapped = False
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
                    if hand_in_yoga_butt_curr_time >= cons.time_tap and not yoga_butt_tapped:
                        # Turn off other buttons
                        some_bttn_active = True

                        # Reset to yoga
                        hand_in_pause_bttn_inittime = cons.num_big
                        hand_in_next_bttn_inittime = cons.num_big

                        # Init variables for first pose 
                        trng_seq = list(detector.poses)
                        #TODO: Get training duration from json
                        pose_name = trng_seq.pop(0)
                        pose_duration = detector.poses[pose_name]['duration']
                        pose_angles = detector.poses[pose_name]['start']['angles']

                        label_next_pose = pose_name.capitalize() + cons.lbl_pose

                        trng_time_left = cons.duration_trng
                        pause_bttn_text_size = cons.fnt_size_timer
                        pause_bttn_curr_rec_width = 0
                        trng_init_time = time.time()
                        prev_trng_curr_time = 0
                        trng_mins, trng_secs = divmod(trng_time_left, 60)
                        pause_bttn_lbl = '{:02d}:{:02d}'.format(trng_mins, trng_secs)

                        pose_time_left = pose_duration
                        next_bttn_curr_rec_width = 0
                        pose_init_time = time.time()
                        prev_pose_curr_time = 0

                        show_paused_bttns = False
                        pause_bttn_active = True
                        pause_bttn_show = True
                        next_bttn_active = True
                        next_bttn_show = True

                        some_bttn_active = False

                        exit_butt_active = False
                        cont_butt_active = False

                        yoga_butt_active = False
                        workout_butt_active = False

                        yoga_active = True
                        workout_active = False
                        
                        yoga_butt_tapped = True

                        cv2.rectangle(img, 
                                (yoga_butt_pos_x, yoga_butt_pos_y), 
                                (yoga_butt_pos_x + yoga_butt_width, yoga_butt_pos_y + yoga_butt_height), 
                                cons.clr_green, 
                                cv2.FILLED)

                else:
                    hand_in_yoga_butt_inittime = time.time()
                    yoga_butt_tapped = False
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
                    if hand_in_workout_butt_curr_time >= cons.time_tap and not workout_butt_tapped:
                        # Turn off other buttons
                        some_bttn_active = True
                        
                        # Reset to yoga
                        hand_in_pause_bttn_inittime = cons.num_big
                        hand_in_next_bttn_inittime = cons.num_big

                        # Init variables for first pose 
                        trng_seq = list(detector.poses)
                        #TODO: Get training duration from json
                        pose_name = trng_seq.pop(0)
                        pose_duration = detector.poses[pose_name]['duration']
                        pose_angles = detector.poses[pose_name]['start']['angles']

                        label_next_pose = pose_name.capitalize() + cons.lbl_pose

                        trng_time_left = cons.duration_trng
                        pause_bttn_text_size = cons.fnt_size_timer
                        pause_bttn_curr_rec_width = 0
                        trng_init_time = time.time()
                        prev_trng_curr_time = 0
                        trng_mins, trng_secs = divmod(trng_time_left, 60)
                        pause_bttn_lbl = '{:02d}:{:02d}'.format(trng_mins, trng_secs)

                        pose_time_left = pose_duration
                        next_bttn_curr_rec_width = 0
                        pose_init_time = time.time()
                        prev_pose_curr_time = 0

                        show_paused_bttns = False
                        pause_bttn_active = True
                        pause_bttn_show = True
                        next_bttn_active = True
                        next_bttn_show = True

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

                        workout_butt_tapped = True

                else:
                    hand_in_workout_butt_inittime = time.time()
                    workout_butt_tapped = False
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