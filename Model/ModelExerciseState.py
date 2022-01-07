class ModelExerciseState():
    """
    Responsible for exercise state data structure
    """
    def __init__(self, name):
        self.name = name
        self.duration = 0
        self.angles = {}
