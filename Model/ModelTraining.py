import json
import os
import Constants as cons
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
            self.duration = -1
            self.exercises = []
            self.curr_exercise = None

            for training_name, exercises in trainings.items():
                # Set training name
                self.name = training_name
                for exercise_name, exercise in exercises.items():
                    if exercise_name == 'duration':
                        # Set training duration
                        self.duration = exercise
                    else:
                        # Init training exercise
                        exer = ModelExercise(exercise_name)
                        for state_name, exercise_state in exercise.items():
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
                        
                        self.exercises.append(exer)    
            self.curr_exercise = exercises.pop(0)
            