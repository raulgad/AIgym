# AIgym - fitness application with personal AI coach

### AIgym was created in order to practise yoga and workout in real time using computer vision
- AIgym supports 2 modes: yoga and workout
- There are 3 exercises in each program:

    Yoga: T-Pose, Warrior Pose, Tree Pose
    
    Workout: Arms, Legs, Push-ups
    
- AIgym was created using [MediaPipe](https://github.com/google/mediapipe), [OpenCV](https://github.com/opencv/opencv), [PyInstaller](https://github.com/pyinstaller/pyinstaller).


### The example of pose handling
![process](static/WarriorPose.gif)

### Remote hand control
![virtual_control](static/hands_control.gif)

### The process of pose recognition consists of the following steps:
- Recieve video stream using OpenCV. 
- Video frames are passed to MediaPipe Pose model that detects pose, adds landmarks and records their coordinates.
- Landmarks coordinates are extracted, organized and passed to the model for prediction.
- The total time of the entire training is displayed in the upper left corner within the "Pause" button (see the gifs above).
- Yoga pose timing and workout repetitions (that user must accomplish) are displayed in the upper right corner within the "Next" button (see the gifs above).


#### This project was completed in 10 days by:
- https://github.com/raulgad
- https://github.com/AugustVIII
- https://github.com/samot-samoe
