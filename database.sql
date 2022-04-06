-- DROP DATABASE team_m_restaurant;

/* creates database */
CREATE DATABASE IF NOT EXISTS `team_m_restaurant` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `team_m_restaurant`;

/* Table Accounts */
CREATE TABLE IF NOT EXISTS `accounts` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
    `fname` varchar(50) NOT NULL,
    `lname` varchar(50) NOT NULL,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
    `email` varchar(100) NOT NULL,
    `phone` varchar(10) NOT NULL,
    `cardnumber` varchar(16),
    `type` varchar(20) DEFAULT 'customer',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Accounts */
-- INSERT INTO accounts VALUES (1, 'manager', 'lmanager', 'admin', 'hd83A3kd', 'admin@onebite.com', '1234567890', NULL, 'manager');
-- INSERT INTO accounts VALUES (2, 'chef1', 'lchef1', 'chef1', 'ds9dajAj', 'chef1@onebite.com', '1234567891', NULL, 'chef');
-- INSERT INTO accounts VALUES (3, 'chef2', 'lchef2', 'chef2', 's9jIdnn1', 'chef2@onebite.com', '1234567892', NULL, 'chef');
-- INSERT INTO accounts VALUES (4, 'delivery1', 'ldelivery1', 'delivery1', 'abc123DE', 'delivery1@onebite.com', '1234567893', NULL, 'delivery');
-- INSERT INTO accounts VALUES (5, 'delivery2', 'ldelivery2', 'delivery2', 'abc123DE', 'delivery2@onebite.com', '1234567894', NULL, 'delivery');
SELECT * FROM accounts;

/* Table Employee */
CREATE TABLE IF NOT EXISTS `employee` (
	`employee_id` int(11) NOT NULL AUTO_INCREMENT,
    `fname` varchar(50) NOT NULL,
    `lname` varchar(50) NOT NULL,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    `phone` varchar(10) NOT NULL,
    `type` varchar(20),
    PRIMARY KEY (`employee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Employee */
INSERT INTO employee(employee_id, fname, lname, username, password, email, phone, type) 
SELECT `id`, `fname`, `lname`, `username`, `password`, `email`, `phone`, `type` 
FROM `accounts` WHERE type = 'manager' or type = 'chef' or type = 'delivery';
SELECT * FROM employee;

/* Table Manager */
CREATE TABLE IF NOT EXISTS `manager` (
	`manager_id` int(11) NOT NULL AUTO_INCREMENT,
    `fname` varchar(50) NOT NULL,
    `lname` varchar(50) NOT NULL,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    `phone` varchar(10) NOT NULL,
    PRIMARY KEY (`manager_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Manager */
INSERT INTO `manager`(`manager_id`, `fname`, `lname`, `username`, `password`, `email`, `phone`) 
SELECT `employee_id`, `fname`, `lname`, `username`, `password`, `email`, `phone` 
FROM `employee` WHERE type = 'manager';
SELECT * FROM manager;

/* Table Chef */
CREATE TABLE IF NOT EXISTS `chef` (
	`chef_id` int(11) NOT NULL AUTO_INCREMENT,
    `fname` varchar(50) NOT NULL,
    `lname` varchar(50) NOT NULL,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    `phone` varchar(10) NOT NULL,
    PRIMARY KEY (`chef_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Chef */
INSERT INTO `chef`(`chef_id`, `fname`, `lname`, `username`, `password`, `email`, `phone`) 
SELECT `employee_id`, `fname`, `lname`, `username`, `password`, `email`, `phone` 
FROM `employee` WHERE type = 'chef';
SELECT * FROM chef;

/* Table Delivery */
CREATE TABLE IF NOT EXISTS `delivery` (
	`delivery_id` int(11) NOT NULL AUTO_INCREMENT,
    `fname` varchar(50) NOT NULL,
    `lname` varchar(50) NOT NULL,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    `phone` varchar(10) NOT NULL,
    PRIMARY KEY (`delivery_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Delivery */
INSERT INTO `delivery`(`delivery_id`, `fname`, `lname`, `username`, `password`, `email`, `phone`) 
SELECT `employee_id`, `fname`, `lname`, `username`, `password`, `email`, `phone` 
FROM `employee` WHERE type = 'delivery';
SELECT * FROM delivery;

/* Table Customer */
CREATE TABLE IF NOT EXISTS `customer` (
	`customer_id` int(11) NOT NULL AUTO_INCREMENT,
    `fname` varchar(50) NOT NULL,
    `lname` varchar(50) NOT NULL,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    `phone` varchar(10) NOT NULL,
    `cardnumber` varchar(16),
    `blacklisted` tinyint(1) DEFAULT 0,
    `vip` tinyint(1) DEFAULT 0,
    PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display Customer */
INSERT INTO `customer`(`customer_id`, `fname`, `lname`, `username`, `password`, `email`, `phone`, `cardnumber`) 
SELECT `id`, `fname`, `lname`, `username`, `password`, `email`, `phone`, `cardnumber`
FROM `accounts` WHERE type = 'customer';
SELECT * FROM customer;

/* Table VIPs */
CREATE TABLE IF NOT EXISTS `vip` (
	`vip_id` int(11) NOT NULL AUTO_INCREMENT,
    `fname` varchar(50) NOT NULL,
    `lname` varchar(50) NOT NULL,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    `phone` varchar(10) NOT NULL,
    `cardnumber` varchar(16),
    PRIMARY KEY (`vip_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Display VIPs */
INSERT INTO `vip`(`vip_id`, `fname`, `lname`, `username`, `password`, `email`, `phone`, `cardnumber`) 
SELECT `customer_id`, `fname`, `lname`, `username`, `password`, `email`, `phone`, `cardnumber`
FROM `customer` WHERE vip = 1;
SELECT * FROM vip;