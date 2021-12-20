# AIgym - fitness application with personal AI trainer.

### AIgym was created in order to practice yoga and workout in real time using computer vision
- AIgym supports 2 modes: yoga and workout
- There are 3 exercises in each program:

    Yoga: T-Pose, Warrior Pose, Tree Pose
    
    Workout: Arms, Legs, Gym
    
- AIgym was created using [MediaPipe](https://github.com/google/mediapipe), [OpenCV](https://github.com/opencv/opencv), [PyInstaller](https://github.com/pyinstaller/pyinstaller).


### Example of pose handling
![process](static/WarriorPose.gif)

### Virtual hands control
![virtual_control](static/hands_control.gif)

### The process of pose recognition consists of following steps:
- Recieve video stream using OpenCV. 
- Video frames are passed to MediaPipe Pose model that detects pose, adds landmarks (33 landmarks per body) and records their coordinates.
- Landmarks coordinates are extracted, organized and passed to the model for prediction.
- The total time of the entire training is animating in the upper left corner above "Pause" button (see gifs above). 
- Yoga pose timing (that user should stands in) or workout's reps is animating in the upper right corner above "Next" button (see gifs above).


#### This project was completed in 10 days by:
- https://github.com/raulgad
- https://github.com/AugustVIII
- https://github.com/samot-samoe
