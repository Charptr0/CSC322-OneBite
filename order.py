import MySQLdb.cursors
from flask_mysqldb import MySQL
from flask import request
from dish import *

class Order():
    def __init__(self, order_id : int, customer_id : int, num_items : int, subtotal : float, tax : float, discount : float, delivery_fee : float, total : float, datetime : str, type : str, status : int, isFree : int):
        '''
        Create a dish object that stores its components

        Parameters
        ----------
        order_id    : int
        customer_id : int
        num_items   : int
        subtotal    : float
        tax         : float
        discount    : float
        delivery_fee: float
        total       : float
        datetime    : str
        type        : str
        status      : boolean
        isFree      : boolean
        '''
        self.order_id = order_id
        self.customer_id = customer_id
        self.num_items = num_items
        self.subtotal = subtotal
        self.tax = tax
        self.discount = discount
        self.delivery_fee = delivery_fee
        self.total = total
        self.datetime = datetime
        self.type = type
        self.status = status
        self.isFree = isFree

    def __str__(self):
        return f'Order ID: {self.order_id}\nCustomer: {self.customer_id}\nNumber of Items: {self.num_items}\nTotal: {str(self.total)}\nType: {self.type}\n\n'

    @staticmethod
    def insertIntoOrders(db : MySQL, user, cartInfo, order_type, datetime, isFree):
        '''
        Inserts new order into a database
        '''
        status = 0
        if order_type == 'pickup':
            status = 1
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO orders (customer_id, num_items, subtotal, tax, discount, total, datetime, type, status, isFree) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                (str(user.id), str(cartInfo["num_items"]), str(cartInfo["subtotal"]), str(cartInfo["tax"]), str(cartInfo["discount"]), str(cartInfo["total"]), datetime, order_type, str(status), str(isFree)))
        cursor.execute('SELECT order_id FROM orders WHERE customer_id = %s ORDER BY order_id DESC', (str(user.id),))
        order_id = cursor.fetchone()
        if isFree == 0 and order_type == 'delivery':
            cursor.execute('INSERT INTO deliveryBid(order_id, customer_id) VALUES (%s, %s)', (str(order_id["order_id"]), str(user.id),))
        db.connection.commit()
        cursor.close()

        return order_id["order_id"]

    @staticmethod
    def insertIntoDetails(db : MySQL, user, order_id, cart):
        '''
        Insert order details into a database
        '''
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        index = 0
        for item in cart["dish"]:
            quantity = cart["quantity"][index]
            cursor.execute('INSERT INTO orderDetails (customer_id, dish_id, quantity) VALUES (%s, %s, %s)', (str(user.id), str(item), str(quantity)))
            index += 1
            cursor.execute('UPDATE orderDetails SET order_id = %s WHERE order_id = 0', (str(order_id),))
        db.connection.commit()
        cursor.close()

    @staticmethod
    def getMostRecentOrder(db, customer_id):
        '''
        Get most recent order from a database

        returns an order object from the database
        '''
        data = []
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        # retrieves most recent order
        cursor.execute('SELECT * FROM orders WHERE customer_id = %s AND status = 0 ORDER BY order_id DESC', (str(customer_id)))
        recent = cursor.fetchall()
        for order in recent:
            # retrieves most recent orders' details
            cursor.execute('SELECT orderDetails.order_id, dish.dish_id, dish.name, dish.price, orderDetails.quantity FROM dish INNER JOIN orderDetails ON dish.dish_id = orderDetails.dish_id WHERE customer_id = %s AND order_id = %s;', (str(customer_id), str(order["order_id"])))
            details = cursor.fetchall()
            data.append(details)
        cursor.close()

        return recent, data

    @staticmethod
    def getPastOrders(db : MySQL, customer_id):
        '''
        Get all past orders except the most recent from a database

        returns a list of orders object from the database
        '''
        data = []

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        # retrieves past order
        cursor.execute('SELECT * FROM orders WHERE customer_id = %s AND status = 1 ORDER BY order_id DESC', (str(customer_id)))
        past = cursor.fetchall()
        for order in past:
            # retrieves completed orders' details
            cursor.execute('SELECT orderDetails.order_id, dish.dish_id, dish.name, dish.price, orderDetails.quantity FROM dish INNER JOIN orderDetails ON dish.dish_id = orderDetails.dish_id WHERE customer_id = %s AND order_id = %s', (str(customer_id), str(order["order_id"])))
            details = cursor.fetchall()
            data.append(details)
        cursor.close()

        return past, data

    @staticmethod
    def getOrderFromID(db : MySQL, id):
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM orders WHERE order_id = %s', (str(id),))
        order = cursor.fetchone()

        cursor.close()
        return Order(order["order_id"], order["customer_id"], order["num_items"], order["subtotal"], order["tax"], order["discount"], 0.0, order["total"], order["type"], order["status"])

    @staticmethod
    def getBid(db : MySQL):
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM deliveryBid INNER JOIN orders ON orders.order_id = deliveryBid.order_id INNER JOIN customer ON orders.customer_id = customer.customer_id INNER JOIN accounts ON orders.customer_id = accounts.id WHERE orders.isFree = 0 and orders.status = 0')
        deliveries = cursor.fetchall()

        cursor.close()
        return deliveries

