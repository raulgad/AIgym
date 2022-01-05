
class ModelTraining():
    """
    Responsible for training data structure
    """
    def __init__(self, data):
        
        self._data = data
        # Convert angle from string to tuple
        for training_type, trainings in self._data.items():

            for training_name, exercises in trainings.items():

                for exercise_name, exercise in exercises.items():

                    if exercise_name == 'duration':
                        pass
                    else:

                        for state_name, exercise_state in exercise.items():
                            
                            if state_name == 'reps':
                                pass
                            else:

                                exercise_state['angles'] = {eval(k):v for k,v in exercise_state['angles'].items()}
