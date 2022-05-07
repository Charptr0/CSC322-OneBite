import json
import MySQLdb.cursors
from flask_mysqldb import MySQL

class Dish():
    def __init__(self, name : str, desc : str, img : str, price : float, id : str, rating : float):
        '''
        Create a dish object that stores its components

        Parameters
        ----------
        name : str
        desc : str
        img (url): str
        price : float
        id : str
        rating : float
        '''
        self.name = name
        self.desc = desc
        self.img = img
        self.price = price
        self.id = id
        self.rating = round(rating)

    def __str__(self):
        return f'Dish Name: {self.name}\n\nDish Desc: {self.desc}\n\nDish Image: {self.img}\n\nDish Price: {str(self.price)}\n'

    @staticmethod
    def getAppetizers(db : MySQL):
        '''
        Get all appetizers from a database

        **FOR TESTING ONLY**
            Get all appetizers from a json file

        returns a list of dish object from the database or json file
        '''
        data = [] # data will be returned

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM dish WHERE dish_type = "appetizer"')
        appetizers = cursor.fetchall()

        for dish in appetizers:
            data.append(Dish(dish["name"], dish["description"], dish["img"], dish["price"], dish["dish_id"], dish["rating"]))

        return data           

    @staticmethod
    def getEntrees(db : MySQL):
        '''
        Get all entrees from a database

        **FOR TESTING ONLY**
            Get all entrees from a json file

        returns a list of dish object from the database or json file
        '''
        data = [] # data will be returned

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM dish WHERE dish_type = "entree"')
        appetizers = cursor.fetchall()

        for dish in appetizers:
            data.append(Dish(dish["name"], dish["description"], dish["img"], dish["price"], dish["dish_id"], dish["rating"]))

        return data 

    @staticmethod
    def getDeserts(db : MySQL):
        '''
        Get all deserts from a database

        **FOR TESTING ONLY**
            Get all deserts from a json file

        returns a list of dish object from the database or json file
        '''
        data = [] # data will be returned

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM dish WHERE dish_type = "dessert"')
        appetizers = cursor.fetchall()

        for dish in appetizers:
            data.append(Dish(dish["name"], dish["description"], dish["img"], dish["price"], dish["dish_id"], dish["rating"]))

        return data

    @staticmethod
    def getDrinks(db):
        '''
        Get all drinks from a database

        **FOR TESTING ONLY**
            Get all drinks from a json file

        returns a list of dish object from the database or json file
        '''
        data = [] # data will be returned

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM dish WHERE dish_type = "drink"')
        appetizers = cursor.fetchall()

        for dish in appetizers:
            data.append(Dish(dish["name"], dish["description"], dish["img"], dish["price"], dish["dish_id"], dish["rating"]))

        return data

    @staticmethod
    def getSpecials(db):
        '''
        Get all specials from a database

        **FOR TESTING ONLY**
            Get all specials from a json file

        returns a list of dish object from the database or json file
        '''
        data = [] # data will be returned

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM dish WHERE dish_type = "special"')
        appetizers = cursor.fetchall()

        for dish in appetizers:
            data.append(Dish(dish["name"], dish["description"], dish["img"], dish["price"], dish["dish_id"], dish["rating"]))

        return data

    @staticmethod
    def getCurrentOrders(db):
        '''
        Get all current order from a database

        **FOR TESTING ONLY**
            Get all current orders from a json file

        returns a list of dish object from the database or json file
        '''
        rawQuery = []  # raw data from the source
        data = []  # data will be returned

        with open("data/currentOrders.json", "r") as f:
            rawQuery = json.load(f)

        for dish in rawQuery:
            data.append(Dish(dish["name"], dish["desc"], dish["img"], dish["price"], dish["id"], dish["rating"]))

        return data

    @staticmethod
    def getPastOrders(db):
        '''
        Get all current order from a database

        **FOR TESTING ONLY**
            Get all current orders from a json file

        returns a list of dish object from the database or json file
        '''
        rawQuery = []  # raw data from the source
        data = []  # data will be returned

        with open("data/pastOrders.json", "r") as f:
            rawQuery = json.load(f)

        for dish in rawQuery:
            data.append(Dish(dish["name"], dish["desc"], dish["img"], dish["price"], dish["id"], dish["rating"]))

        return data

    @staticmethod
    def getPopularDishes(db):
        '''
        Get all current order from a database

        **FOR TESTING ONLY**
            Get all current orders from a json file

        returns a list of dish object from the database or json file
        '''
        rawQuery = []  # raw data from the source
        data = []  # data will be returned

        with open("data/popular_dishes.json", "r") as f:
            rawQuery = json.load(f)

        for dish in rawQuery:
            data.append(Dish(dish["name"], dish["desc"], dish["img"], dish["price"], dish["id"], dish["rating"]))

        return data