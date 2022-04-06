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
        userType : str
        '''
        super().__init__(**kwargs)

        try:
            self.cardNumber = kwargs["cardNumber"]
        except KeyError:
            self.cardNumber = None

    def setCardNumber(self, db, cardNumber = None):
        if cardNumber == None:
            return

        self.cardNumber = cardNumber

    def setName(self, db, firstName = None, lastName = None):
        if firstName == None or lastName == None:
            return

        # DB stuff go here

        super().setName(firstName, lastName)

    def setEmail(self, db, email = None):
        '''
        Update the user's email
        '''
        if email == None:
            return

        # DB stuff go here

        super().setEmail(email)

    def setUsername(self, db, username = None):
        '''
        Update the user's username
        '''
        if username == None:
            return

        super().setUsername(username)

    def setPhoneNumber(self, db, phoneNumber = None):
        '''
        Update the user's phone number
        '''
        if phoneNumber == None:
            return

        super().setPhoneNumber(phoneNumber)        
        