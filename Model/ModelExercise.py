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
        self.state_idx = 0
    
    def set_next_state(self):
        if self.state_idx < len(self.states): 
            self.state = self.states[self.state_idx]
            self.state_idx += 1
        else:
            self.state = None
    
    def reset_state(self):
        self.state_idx = 0
        self.state = self.states[self.state_idx]
        