import MySQLdb.cursors
from flask_mysqldb import MySQL
from dish import *

class Order():
    def __init__(self, order_id : int, customer_id : int, num_items : int, subtotal : float, tax : float, discount : float, delivery_fee : float, total : float, type : str, status : int):
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
        type        : str
        status      : boolean
        '''
        self.order_id = order_id
        self.customer_id = customer_id
        self.num_items = num_items
        self.subtotal = subtotal
        self.tax = tax
        self.discount = discount
        self.delivery_fee = delivery_fee
        self.total = total
        self.type = type
        self.status = status

    def __str__(self):
        return f'Order ID: {self.order_id}\nCustomer: {self.customer_id}\nNumber of Items: {self.num_items}\nTotal: {str(self.total)}\nType: {self.type}\n\n'

    @staticmethod
    def insertIntoOrders(db : MySQL, user, cart, cartInfo, order_type):
        '''
        Inserts new order into a database
        '''
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO orders (customer_id, num_items, subtotal, tax, discount, total, type, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', 
                    (str(user.id), str(len(cart["dish"])), str(cartInfo["subtotal"]), str(cartInfo["tax"]), str(cartInfo["discount"]), str(cartInfo["total"]), order_type, str(0)))
        cursor.execute('SELECT order_id FROM orders WHERE customer_id = %s ORDER BY order_id DESC', (str(user.id),))
        order_id = cursor.fetchone()
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

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        # retrieves most recent order
        cursor.execute('SELECT * FROM orders WHERE customer_id = %s ORDER BY order_id DESC', (str(customer_id)))
        recent = cursor.fetchone()

        # retrieves most recent order's details
        cursor.execute('SELECT dish.dish_id, dish.name, dish.price, orderDetails.quantity FROM dish INNER JOIN orderDetails ON dish.dish_id = orderDetails.dish_id WHERE customer_id = %s AND order_id = %s;', (str(customer_id), str(recent["order_id"])))
        details = cursor.fetchall()
        
        cursor.close()

        return recent, details

    @staticmethod
    def getPastOrders(db : MySQL, customer_id):
        '''
        Get all past orders except the most recent from a database

        returns a list of orders object from the database
        '''
        data = []

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        # retrieves past order
        cursor.execute('SELECT * FROM orders WHERE customer_id = %s ORDER BY order_id DESC LIMIT 1, 1000', (str(customer_id)))
        past = cursor.fetchall()
        for order in past:
            # retrieves most recent order's details
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