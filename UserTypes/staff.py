from user import User

class Staff(User):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)