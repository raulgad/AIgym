import json
import os
import math
import logging
import Constants as cons
import Controller.Detector as detector
from Model.ModelExercise import ModelExercise
from Model.ModelExerciseState import ModelExerciseState

class ModelTraining():
    """
    Responsible for training data structure
    """
    def __init__(self, type):
        # Parse data
        with open(os.path.join(os.path.dirname(__file__), cons.file_training), 'r') as fp:
            data = json.load(fp)
            trainings = data['yoga' if type else 'workout']
            # Set all training variables
            self.name = ''
            self.duration = 0
            self.exercises = []
            # Init current exercise
            self.exercise = None

            for training_name, exercises in trainings.items():
                # Set training name
                self.name = training_name
                for exercise_name, _exercise in exercises.items():
                    if exercise_name == 'duration':
                        # Set training duration
                        self.duration = _exercise
                    else:
                        # Init training exercise
                        exer = ModelExercise(exercise_name)
                        for state_name, exercise_state in _exercise.items():
                            if state_name == 'reps':
                                # Set exercise repititions
                                exer.reps = exercise_state
                            else:
                                # Add exercise state if state has angles
                                if exercise_state['angles']:
                                    exer_state  = ModelExerciseState(state_name)
                                    exer_state.duration =  exercise_state['duration']
                                    # Convert angle from string to tuple
                                    exer_state.angles = {eval(k):v for k,v in exercise_state['angles'].items()}
                                    exer.states.append(exer_state)
                                    # Increase exercise duration
                                    exer.duration += exer_state.duration
                        exer.state = exer.states.pop(0)
                        self.exercises.append(exer)
            self.exercise = self.exercises.pop(0)
    
    def set_next_exercise(self):
        if self.exercises: 
            self.exercise = self.exercises.pop(0) 
            # Set exercise duration
            for state in self.exercise.states: self.exercise.duration += state.duration
        else:   
            self.exercise = None

    def find_angle(self, points):
        # Get the coordinates
        x1, y1, _ = detector.lmks[points[0]]
        x2, y2, _ = detector.lmks[points[1]]
        x3, y3, _ = detector.lmks[points[2]]
        # Calculate the angle between three coordinates
        return abs(math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)))
    
    def incorr_angs(self, angles, angle_gap = 20):
        # Init dictionary of user's current incorrect angles
        incorr_angs = {}
        try:
            # Check each current angle if it's same as correct
            for ang_ids, ang in angles.items():
                # Get current user's angle from it's points
                curr_ang = self.find_angle(ang_ids)
                # Check if current user angle is in suitable range
                if abs(curr_ang - ang) <= angle_gap:
                    # Remove the angle that has become correct, for not drawing it later
                    if ang_ids in incorr_angs:
                        del incorr_angs[ang_ids]
                # Add angle that user should do
                else:
                    incorr_angs[ang_ids] = ang
            return incorr_angs
        except:
            logging.debug('Something goes wrong in correct_pose() -> ModelTraining')
            return incorr_angs