from staff import Staff

class Manager(Staff):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)