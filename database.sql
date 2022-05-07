-- DROP DATABASE team_m_restaurant;

/* creates database */
CREATE DATABASE IF NOT EXISTS team_m_restaurant DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE team_m_restaurant;

/* Table Accounts */
CREATE TABLE IF NOT EXISTS accounts (
	id int(11) NOT NULL AUTO_INCREMENT,
    fname varchar(50) NOT NULL,
    lname varchar(50) NOT NULL,
    username varchar(50) NOT NULL,
  	password varchar(255) NOT NULL,
    email varchar(100) NOT NULL,
    phone varchar(10) NOT NULL,
    type varchar(20) DEFAULT 'customer',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Accounts */
INSERT INTO accounts VALUES (1, 'manager', 'lmanager', 'admin', '123abcABC', 'admin@onebite.com', '1234567890', 'manager');
INSERT INTO accounts VALUES (2, 'chef1', 'lchef1', 'chef1', '123abcABC', 'chef1@onebite.com', '1234567891', 'chef');
INSERT INTO accounts VALUES (3, 'chef2', 'lchef2', 'chef2', '123abcABC', 'chef2@onebite.com', '1234567892', 'chef');
INSERT INTO accounts VALUES (4, 'delivery1', 'ldelivery1', 'delivery1', '123abcABC', 'delivery1@onebite.com', '1234567893', 'delivery');
INSERT INTO accounts VALUES (5, 'delivery2', 'ldelivery2', 'delivery2', '123abcABC', 'delivery2@onebite.com', '1234567894', 'delivery');
SELECT * FROM accounts;

/* Table Employee */
CREATE TABLE IF NOT EXISTS employee (
	employee_id int(11) NOT NULL AUTO_INCREMENT,
    fname varchar(50) NOT NULL,
    lname varchar(50) NOT NULL,
    username varchar(50) NOT NULL,
  	password varchar(255) NOT NULL,
    email varchar(100) NOT NULL,
    phone varchar(10) NOT NULL,
    type varchar(20),
    PRIMARY KEY (employee_id),
    FOREIGN KEY (employee_id) REFERENCES accounts(id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Employee */
INSERT INTO employee(employee_id, fname, lname, username, password, email, phone, type) 
SELECT id, fname, lname, username, password, email, phone, type
FROM accounts WHERE type = 'manager' or type = 'chef' or type = 'delivery';
SELECT * FROM employee;

/* Table Chef */
CREATE TABLE IF NOT EXISTS chef (
	chef_id int(11) NOT NULL AUTO_INCREMENT,
    salary float(11, 2) DEFAULT '5500.00',
	num_compliment int(11) DEFAULT 0,
    num_complaint int(11) DEFAULT 0,
    warnings int(11) DEFAULT 0,
    demotions int(11) DEFAULT 0,
    PRIMARY KEY (chef_id),
    FOREIGN KEY (chef_id) REFERENCES employee(employee_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Chef */
INSERT INTO chef(chef_id) 
SELECT employee_id FROM employee WHERE type = 'chef';
SELECT * FROM chef;

/* Table Delivery */
CREATE TABLE IF NOT EXISTS delivery (
	delivery_id int(11) NOT NULL AUTO_INCREMENT,
    salary float(11, 2) DEFAULT '4000.00',
	num_compliment int(11) DEFAULT 0,
    num_complaint int(11) DEFAULT 0,
    warnings int(11) DEFAULT 0,
    demotions int(11) DEFAULT 0,
    PRIMARY KEY (delivery_id),
    FOREIGN KEY (delivery_id) REFERENCES employee(employee_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Delivery */
INSERT INTO delivery(delivery_id) 
SELECT employee_id FROM employee WHERE type = 'delivery';
SELECT * FROM delivery;

/* Table Customer */
CREATE TABLE IF NOT EXISTS customer (
	customer_id int(11) NOT NULL AUTO_INCREMENT,
    wallet float(7, 2) DEFAULT '0.00',
    cardnumber varchar(16),
    address text,
    num_orders int(11) DEFAULT 0,
    total_spent float(11, 2) DEFAULT '0.00',
    warnings int(11) DEFAULT 0,
    isBlacklisted tinyint(1) DEFAULT 0,
    isVIP tinyint(1) DEFAULT 0,
    PRIMARY KEY (customer_id),
    FOREIGN KEY (customer_id) REFERENCES accounts(id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Customer */
SELECT * FROM customer;

/* Table VIPs */
CREATE TABLE IF NOT EXISTS vip (
	vip_id int(11) NOT NULL AUTO_INCREMENT,
    num_orders int(11) DEFAULT 0,
    num_free_deliveries int(11) DEFAULT 0,
    warnings int(11) DEFAULT 0,
    PRIMARY KEY (vip_id),
    FOREIGN KEY (vip_id) REFERENCES customer(customer_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display VIPs */
INSERT INTO vip(vip_id) 
SELECT customer_id FROM customer WHERE isVIP = 1;
SELECT * FROM vip;

/* Table Dishes */
CREATE TABLE IF NOT EXISTS dish (
	dish_id int(11) NOT NULL AUTO_INCREMENT,
    dish_type varchar(50) NOT NULL,
    name varchar(100) NOT NULL,
	price float(6, 2) NOT NULL DEFAULT '0.00',
    description text NOT NULL,
	img text NOT NULL,
    chef int(11) NOT NULL,
    rating int(11) NOT NULL DEFAULT 0,
    num_ratings int(11) NOT NULL DEFAULT 0,
    count int(11) NOT NULL DEFAULT 0,
    status tinyint(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (dish_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Dishes */
INSERT INTO dish VALUES (1, 'special', 'Oven-Baked Pizza', '15.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1589477500339-82aeb8718167?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 2, 0, 0, 0, 1);
INSERT INTO dish VALUES (2, 'special', 'Cheeseburger with Fries', '14.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1600688640154-9619e002df30?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=654&q=800', 2, 0, 0, 0, 1);
INSERT INTO dish VALUES (3, 'special', 'Lemon Pepper Spaghetti', '14.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1481931098730-318b6f776db0?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=780&q=80', 2, 0, 0, 0, 1);
INSERT INTO dish VALUES (4, 'special', 'Pasta Carbonara', '14.50', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1546549032-9571cd6b27df?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 2, 0, 0, 0, 1);
INSERT INTO dish VALUES (5, 'special', 'Donut of the Day', '8.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1618411640018-972400a01458?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 0, 0, 0, 1);
INSERT INTO dish VALUES (6, 'special', 'Pie of the Week', '9.50', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1535920527002-b35e96722eb9?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 0, 0, 0, 1);
INSERT INTO dish VALUES (7, 'special', 'Caramel Cheesecake', '9.25', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1547414368-ac947d00b91d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80', 3, 0, 0, 0, 1);
INSERT INTO dish VALUES (8, 'special', 'Ferrero Chocolate Milkshake', '7.50', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1594488506255-a8bbfdeedbaf?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 0, 0, 0, 1);
INSERT INTO dish VALUES (9, 'appetizer', 'Acai Bowl', '6.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1590301157284-ab2f8707bdc1?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80', 2, 0, 0, 0, 1);
INSERT INTO dish VALUES (10, 'appetizer', 'Classic Caesar Salad', '8.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1594834749740-74b3f6764be4?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=782&q=80', 2, 0, 0, 0, 1);
INSERT INTO dish VALUES (11, 'appetizer', 'Eggs Benedict', '7.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1608039829572-78524f79c4c7?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 2, 0, 0, 0, 1);
INSERT INTO dish VALUES (12, 'appetizer', 'Pita Chips and Spinach Dip', '4.50', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1627308595127-d9acf19107ce?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80', 2, 0, 0, 0, 1);
INSERT INTO dish VALUES (13, 'entree', 'Blueberry Pancakes', '9.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1506084868230-bb9d95c24759?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 2, 0, 0, 0, 1);
INSERT INTO dish VALUES (14, 'entree', 'French Toast', '10.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1484723091739-30a097e8f929?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=898&q=80', 2, 0, 0, 0, 1);
INSERT INTO dish VALUES (15, 'entree', 'Fresh Crepes', '8.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1519676867240-f03562e64548?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 2, 0, 0, 0, 1);
INSERT INTO dish VALUES (16, 'entree', 'Croissant Sandwich', '11.50', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1600761857007-5f51d5dc82a0?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 2, 0, 0, 0, 1);
INSERT INTO dish VALUES (17, 'entree', 'Pulled Pork Sourdough Toast', '13.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1559054663-e8d23213f55c?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 2, 0, 0, 0, 1);
INSERT INTO dish VALUES (18, 'entree', 'Smoked Salmon Sourdough Toast', '13.50', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1627308595216-439c00ade0fe?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80', 2, 0, 0, 0, 1);
INSERT INTO dish VALUES (19, 'dessert', 'Black Cherry Chocolate Tart', '4.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1547043184-599cd7e6acb9?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 0, 0, 0, 1);
INSERT INTO dish VALUES (20, 'dessert', 'Blackberry Lemon Tart', '4.50', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1560180474-e8563fd75bab?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 0, 0, 0, 1);
INSERT INTO dish VALUES (21, 'dessert', 'Blueberry Cheesecake', '8.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1567327613485-fbc7bf196198?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 0, 0, 0, 1);
INSERT INTO dish VALUES (22, 'dessert', 'Lemon Meringue Pie', '8.50', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1519915028121-7d3463d20b13?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 0, 0, 0, 1);
INSERT INTO dish VALUES (23, 'dessert', 'Peach Pavlova', '7.25', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1624300603538-1207400f4116?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 0, 0, 0, 1);
INSERT INTO dish VALUES (24, 'dessert', 'Strawberry Panna Cotta', '5.50', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1488477181946-6428a0291777?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 0, 0, 0, 1);
INSERT INTO dish VALUES (25, 'drink', 'Coffee', '4.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1540692802289-42509772934e?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 0, 0, 0, 1);
INSERT INTO dish VALUES (26, 'drink', 'Hot Chocolate', '5.00', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas! Earum repellat dicta natus accusantium recusandae necessitatibus veniam!', 'https://images.unsplash.com/photo-1548329408-0bcd6e68058d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 0, 0, 0, 1);
INSERT INTO dish VALUES (27, 'drink', 'Blackberry Lemonade', '5.75', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1560179304-6fc1d8749b23?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 0, 0, 0, 1);
INSERT INTO dish VALUES (28, 'drink', 'Blueberry Limeade', '5.75', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam eum error maiores laudantium odit ab sequi sed, distinctio, asperiores pariatur accusamus quas!', 'https://images.unsplash.com/photo-1504310578167-435ac09e69f3?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80', 3, 0, 0, 0, 1);
SELECT * FROM dish;