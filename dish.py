import json

class Dish():
    def __init__(self, name : str, desc : str, img : str, price : float):
        '''
        Create a dish object that stores its components

        Parameters
        ----------
        name : str
        desc : str
        img (url): str
        price : float
        '''
        self.name = name
        self.desc = desc
        self.img = img
        self.price = price

    def __str__(self):
        return f'Dish Name: {self.name}\n\nDish Desc: {self.desc}\n\nDish Image: {self.img}\n\nDish Price: {str(self.price)}\n'

    @staticmethod
    def getAppetizers(db):
        '''
        Get all appetizers from a database

        **FOR TESTING ONLY**
            Get all appetizers from a json file

        returns a list of dish object from the database or json file
        '''
        rawQuery = [] # raw data from the source
        data = [] # data will be returned

        with open("data/appetizers.json", "r") as f:
            rawQuery = json.load(f)

        for dish in rawQuery:
            data.append(Dish(dish["name"], dish["desc"], dish["img"], dish["price"]))

        return data            

    @staticmethod
    def getEntrees(db):
        '''
        Get all entrees from a database

        **FOR TESTING ONLY**
            Get all entrees from a json file

        returns a list of dish object from the database or json file
        '''
        rawQuery = []
        data = []

        with open("data/entrees.json", "r") as f:
            rawQuery = json.load(f)

        for dish in rawQuery:
            data.append(Dish(dish["name"], dish["desc"], dish["img"], dish["price"]))

        return data 

    @staticmethod
    def getDeserts(db):
        '''
        Get all deserts from a database

        **FOR TESTING ONLY**
            Get all deserts from a json file

        returns a list of dish object from the database or json file
        '''
        rawQuery = []
        data = []

        with open("data/entrees.json", "r") as f:
            rawQuery = json.load(f)

        for dish in rawQuery:
            data.append(Dish(dish["name"], dish["desc"], dish["img"], dish["price"]))

        return data 

    @staticmethod
    def getPopularDishes(db):
        '''
        Get the current popular dishes from a database

        **FOR TESTING ONLY**
            Get all deserts from a json file

        returns a list of dish object from the database or json file
        '''
        rawQuery = []
        data = []

        with open("data/popular_dishes.json", "r") as f:
            rawQuery = json.load(f)

        for dish in rawQuery:
            data.append(Dish(dish["name"], dish["desc"], dish["img"], dish["price"]))

        return data 
