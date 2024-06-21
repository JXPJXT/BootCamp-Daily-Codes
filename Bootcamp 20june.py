# Create database
CREATE DATABASE rapido;
USE rapido;

# Restaurants - rid, rname, location (e.g., New York, San Francisco)
CREATE TABLE restaurants
(
    rid INT(3) PRIMARY KEY,
    rname VARCHAR(50) NOT NULL,
    location VARCHAR(30)
);

# Dishes - did, dname, price, stock, rid
CREATE TABLE dishes
(
    did INT(3) PRIMARY KEY,
    dname VARCHAR(50) NOT NULL,
    price INT(10) NOT NULL,
    stock INT(5),
    rid INT(3),
    FOREIGN KEY (rid) REFERENCES restaurants(rid)
);

# Customers - cid, cname, age, addr
CREATE TABLE customers
(
    cid INT(3) PRIMARY KEY,
    cname VARCHAR(30) NOT NULL,
    age INT(3),
    addr VARCHAR(50)
);

# Orders - oid, cid, did, amt
CREATE TABLE orders
(
    oid INT(3) PRIMARY KEY,
    cid INT(3),
    did INT(3),
    amt INT(10) NOT NULL,
    FOREIGN KEY (cid) REFERENCES customers(cid),
    FOREIGN KEY (did) REFERENCES dishes(did)
);

# Payments - pay_id, oid, amount, mode (cash, card, upi), status
CREATE TABLE payments
(
    pay_id INT(3) PRIMARY KEY,
    oid INT(3),
    amount INT(10) NOT NULL,
    mode VARCHAR(30) CHECK (mode IN ('cash', 'card', 'upi')),
    status VARCHAR(30),
    timestamp TIMESTAMP,
    FOREIGN KEY (oid) REFERENCES orders(oid)
);

# Inserting values into restaurants table
INSERT INTO restaurants VALUES (1, 'Burger King', 'New York');
INSERT INTO restaurants VALUES (2, 'Pizza Hut', 'San Francisco');
INSERT INTO restaurants VALUES (3, 'Taco Bell', 'New York');
INSERT INTO restaurants VALUES (4, 'Subway', 'San Francisco');
INSERT INTO restaurants VALUES (5, 'KFC', 'New York');

# Inserting values into dishes table
INSERT INTO dishes VALUES (1, 'Whopper', 500, 20, 1);
INSERT INTO dishes VALUES (2, 'Pepperoni Pizza', 600, 15, 2);
INSERT INTO dishes VALUES (3, 'Crunchy Taco', 300, 30, 3);
INSERT INTO dishes VALUES (4, 'Italian BMT', 400, 25, 4);
INSERT INTO dishes VALUES (5, 'Fried Chicken', 450, 10, 5);

# Inserting values into customers table
INSERT INTO customers VALUES (101, 'Alice', 30, '123 Main St');
INSERT INTO customers VALUES (102, 'Bob', 25, '456 Elm St');
INSERT INTO customers VALUES (103, 'Charlie', 35, '789 Oak St');
INSERT INTO customers VALUES (104, 'Diana', 28, '101 Maple St');
INSERT INTO customers VALUES (105, 'Eve', 22, '202 Pine St');

# Inserting values into orders table
INSERT INTO orders VALUES (10001, 101, 1, 500);
INSERT INTO orders VALUES (10002, 102, 2, 600);
INSERT INTO orders VALUES (10003, 103, 3, 300);
INSERT INTO orders VALUES (10004, 104, 4, 400);
INSERT INTO orders VALUES (10005, 105, 5, 450);

# Inserting values into payments table
INSERT INTO payments VALUES (1, 10001, 500, 'cash', 'completed', '2024-06-01 08:00:00');
INSERT INTO payments VALUES (2, 10002, 600, 'card', 'completed', '2024-06-01 08:10:00');
INSERT INTO payments VALUES (3, 10003, 300, 'upi', 'completed', '2024-06-01 08:15:00');
INSERT INTO payments VALUES (4, 10004, 400, 'cash', 'pending', '2024-06-01 08:20:00');
INSERT INTO payments VALUES (5, 10005, 450, 'card', 'completed', '2024-06-01 08:25:00');

# Queries
# Subqueries
# 1. Find the customer who placed the order with the highest total amount.
SELECT cname 
FROM customers 
WHERE cid = (
    SELECT cid 
    FROM orders 
    GROUP BY cid 
    ORDER BY SUM(amt) DESC 
    LIMIT 1
);

# 2. Retrieve the names of all customers who have placed orders for dishes located in the same city as the customer named "Bob".
SELECT cname
FROM customers
WHERE cid IN (
    SELECT DISTINCT cid
    FROM orders
    WHERE did IN (
        SELECT did
        FROM dishes
        WHERE rid = (
            SELECT rid
            FROM restaurants
            WHERE location = (
                SELECT location
                FROM customers
                WHERE cname = 'Bob'
            )
        )
    )
);

# 3. Retrieve the names of all customers who have placed orders for dishes that have a price higher than the average price of dishes bought by each customer.
SELECT cname
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM orders o
    JOIN dishes d ON o.did = d.did
    WHERE o.cid = c.cid
    AND d.price > (
        SELECT AVG(price)
        FROM dishes
        WHERE did IN (
            SELECT did
            FROM orders
            WHERE cid = c.cid
        )
    )
);

# 4. Retrieve the names of customers who have placed orders for dishes with a price higher than the average price of all dishes in the same city as the customer, and also display the total amount spent by each customer on such orders.
SELECT c.cname, SUM(o.amt) AS total_amount_spent
FROM customers c
INNER JOIN orders o ON c.cid = o.cid
INNER JOIN dishes d ON o.did = d.did
INNER JOIN restaurants r ON d.rid = r.rid
INNER JOIN (
    SELECT location, AVG(price) AS avg_price
    FROM dishes d
    JOIN restaurants r ON d.rid = r.rid
    GROUP BY location
) avg_prices ON r.location = avg_prices.location
WHERE d.price > avg_prices.avg_price
GROUP BY c.cname;

# 5. Retrieve the names of all customers along with the total amount they have spent on orders, including customers who have not placed any orders yet.
SELECT c.cname, COALESCE(SUM(o.amt), 0) AS total_amount_spent
FROM customers c
LEFT JOIN orders o ON c.cid = o.cid
GROUP BY c.cname;
