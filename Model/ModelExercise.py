class ModelExercise():
    """
    Responsible for exercise data structure
    """
    def __init__(self, name):
        self.name = name
        self.duration = 0
        self.reps = 0
        self.states = []
        # Init current state
        self.state = None
    
    def set_next_state(self):
        self.state = self.states.pop(0) if self.states else None