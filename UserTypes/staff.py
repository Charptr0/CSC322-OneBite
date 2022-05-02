from user import User

class Staff(User):
    '''
    Create a staff in session

    DO NOT INSTANTIATE 

    Parameters
    ----------
    id : int
    firstName : str
    lastName : str
    email : str
    uname : str
    password : str
    phoneNumber : str
    userType : str
    
    salary : float
    compliments : int
    complaints : int
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        try:
            self._salary = kwargs["salary"]
        except KeyError:
            self._salary = 0
        
        self.compliments = 0
        self.complaints = 0