from user import User

class Customer(User):
    def __init__(self, **kwargs):
        '''
        Create a new customer in session

        Parameters:
        ----------
        id : int
        firstName : str
        lastName : str
        email : str
        uname : str
        password : str
        phoneNumber : str
        cardNumber : str
        type : str
        isVIP : boolean
        wallet : float
        address : str
        orders : array of Dishes
        '''
        super().__init__(**kwargs)

        try:
            self.cardNumber = kwargs["cardNumber"]
        except KeyError:
            self.cardNumber = None

        try:
            self.isVIP = kwargs["isVIP"]
        except KeyError:
            self.isVIP = False

        try:
            self.wallet = kwargs["wallet"]
        except KeyError:
            self.isVIP = 0.0

        try:
            self.address = kwargs["address"]
        except KeyError:
            self.address = None

        self.warnings = 0
        self.orders = []

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

    def getFavoriteDishes(self, db):
        '''
        Get and set the user's top dishes
        '''       

        self.favoriteDishes = [
            {"name" : "Dish 1", "desc" : "Desc 1", "img" : "../static/assets/test.jpg", "price" : "$10"},
            {"name" : "Dish 1", "desc" : "Desc 1", "img" : "../static/assets/test.jpg", "price" : "$10"},
            {"name" : "Dish 1", "desc" : "Desc 1", "img" : "../static/assets/test.jpg", "price" : "$10"},
        ]

        return self.favoriteDishes

    def addOrder(self, dish_id):
        self.orders.append(dish_id)

        