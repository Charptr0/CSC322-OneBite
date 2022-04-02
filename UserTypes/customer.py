from user import User

class Customer(User):
    def __init__(self, **kwargs):
        '''
        Create a new customer in session

        Parameters:
        ----------
        firstName : str
        lastName : str
        email : str
        uname : str
        password : str
        phoneNumber : str
        cardNumber : str
        '''
        super().__init__(**kwargs)
        self.cardNumber = kwargs["cardNumber"]

    def setCardNumber(self, db, cardNumber = None):
        if cardNumber == None:
            return

        self.cardNumber = cardNumber
        