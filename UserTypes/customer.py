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
        username : str
        password : str
        phoneNumber : str
        cardNumber : str
        type : str
        isVIP : boolean
        wallet : float
        address : str
        num_orders : int
        total_spent : float
        warnings : int
        isBlacklisted : boolean
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
            self.isVIP = 0

        try:
            self.wallet = kwargs["wallet"]
        except KeyError:
            self.wallet = 0.0

        try:
            self.address = kwargs["address"]
        except KeyError:
            self.address = None

        try:
            self.num_orders = kwargs["num_orders"]
        except KeyError:
            self.num_orders = 0

        try:
            self.total_spent = kwargs["total_spent"]
        except KeyError:
            self.total_spent = 0.0

        try:
            self.warnings = kwargs["warnings"]
        except KeyError:
            self.warnings = 0

        try:
            self.isBlacklisted = kwargs["isBlacklisted"]
        except KeyError:
            self.isBlacklisted = 0

        self.orders = []

    def setCardNumber(self, db, cardNumber = None):
        if cardNumber == None:
            return

        self.cardNumber = cardNumber

    def setisVIP(self, db, isVIP = None):
        if isVIP == None:
            return

        self.isVIP = isVIP

    def setWallet(self, db, wallet = None):
        if wallet == None:
            return

        self.wallet = wallet
    
    def setAddress(self, db, address = None):
        if address == None:
            return

        self.address = address

    def setNumOrders(self, db, num_orders = None):
        if num_orders == None:
            return

        self.num_orders = num_orders

    def setTotalSpent(self, db, total_spent = None):
        if total_spent == None:
            return

        self.total_spent = total_spent

    def setWarnings(self, db, warnings = None):
        if warnings == None:
            return

        self.warnings = warnings

    def setisBlacklisted(self, db, isBlacklisted = None):
        if isBlacklisted == None:
            return

        self.isBlacklisted = isBlacklisted

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

        