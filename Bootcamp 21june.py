use rapido;
-- DELIMITER COMMAND:
/*
1. Purpose: 
   - The DELIMITER command is used to change the standard delimiter(like a semicolon (;)), to a different character. 
2. Usage:
   - When defining stored procedures, functions, or other multi-statement constructs that contain semicolons within their body.
   - This allows you to specify a different character as the delimiter to avoid prematurely terminating the entire statement.
3. Syntax:
   - The syntax for the DELIMITER command is as follows:
     DELIMITER new_delimiter;
4. Example:
   - Changing the delimiter to //:
     DELIMITER //
     CREATE PROCEDURE procedure_name()
     BEGIN
			SQL statements
     END //
     DELIMITER ;

5. Resetting the delimiter:
   - After defining the stored procedure or function, you should reset the delimiter back to the standard semicolon (;) using:
     DELIMITER ;
*/

-- DETERMINISTIC: 
 /*
DETERMINISTIC indicates that the function will always return the same result for the same input values.
If the function contains any non-deterministic elements (e.g., calls to functions that return different values each time they are called),
you should omit this keyword.
*/


-- PROCEDURES 
 /*  A procedure is a set of SQL statements that can be saved and reused.
  ~ Procedures can have input parameters (IN) and output parameters (OUT).
  ~ Procedures do not return a value.
  ~ A procedure is a prepared SQL code that you can save, so the code can be reused over and over again.
  ~ So if you have an SQL query that you write over and over again, save it as a stored procedure, and then just call it to execute it. */
 
 
-- CREATE PROCEDURE
/* 
Procedures in SQL allow you to encapsulate a series of SQL statements into a reusable unit.
~ Syntax:
	DELIMITER //
		CREATE PROCEDURE procedure_name(parameter1 datatype, parameter2 datatype, ...)
		BEGIN
			Procedure logic goes here
		END //
	DELIMITER ;
*/ 

-- EXAMPLE:
-- Procedure to select all products 
DELIMITER //
CREATE PROCEDURE select_all_products()
BEGIN
    SELECT * FROM products;
END //
DELIMITER ;


-- EXECUTING PROCEDURES
/*
Once a procedure is created, you can execute it using the CALL statement followed by the procedure name and any required parameters.
~ Syntax:
-- CALL procedure_name(parameter1, parameter2, ...);
*/

-- EXAMPLE:
-- Calling the select_all_products procedure
CALL select_all_products();


-- DROPPING PROCEDURES
/*
If a procedure is no longer needed, it can be dropped using the DROP PROCEDURE statement.
~ Syntax: 
	DROP PROCEDURE procedure_name;
*/

-- EXAMPLE:
-- Dropping select_all_products
DROP PROCEDURE select_all_products;


-- FUNCTIONS
/*
A function is a reusable block of code that performs a specific task and can return a value.
Functions are similar to procedures, but procedures do not return values.
Functions can have input parameters (IN) but cannot have output parameters.
Input parameters allow you to pass data into the function, and the function can use that data to perform its task.
*/

-- FUNCTION CREATION
/*
To create a function, you need to define its name, input parameters (if any), and the data type of the value it returns.
The function logic (the code that performs the task) goes inside the BEGIN and END blocks.

Syntax:
CREATE FUNCTION function_name(parameter1 data_type, parameter2 data_type, ...)
RETURNS return_data_type
AS
BEGIN
    -- Function logic here
END;
*/

-- EXAMPLE:
-- Function to calculate total revenue for a product
DELIMITER $$
CREATE FUNCTION get_total_revenue()
RETURNS INT
DETERMINISTIC 
BEGIN
DECLARE total_revenue INT; 
-- Declare a variable to store the total revenue
-- Calculate the total revenue by summing the 'amount' column from the 'payment' table
-- for all completed orders
SELECT SUM(p.amount) INTO total_revenue
FROM payment p
INNER JOIN orders o ON p.oid = o.oid
WHERE p.status = 'completed';
RETURN total_revenue; -- Returns the calculated total revenue
END$$
DELIMITER ;
-- Restores the original delimiter


-- FUNCTION EXECUTION
/*
To execute (call) a function, you use the SELECT statement along with the function name and any required input parameters.
Syntax:
SELECT function_name(parameter1, parameter2, ...);
*/

-- EXAMPLE:
-- Calling the function
SELECT get_total_revenue(); -- This will execute the function and return the total revenue


-- DROPPING FUNCTION
/*
If you no longer need a function, you can drop (delete) it using the DROP FUNCTION statement.
Syntax:
DROP FUNCTION [IF EXISTS] function_name;
The IF EXISTS clause is optional and allows you to avoid an error if the function doesn't exist.
*/

-- EXAMPLE:
-- Dropping the function
DROP FUNCTION IF EXISTS get_total_revenue;
-- This will remove the 'get_total_revenue' function from the database


-- IN
/* 
This In is a  part of procedures
IN parameters in MySQL stored procedures allow you to pass values into the procedure.
These values are read-only within the procedure and cannot be modified
 */
 
/* 
~ Syntax for IN
 CREATE PROCEDURE procedure_name(IN parameter_name data_type)
 BEGIN
    -- Procedure logic using parameter_name
    END;
*/

-- Creating procedure with IN
DELIMITER //
CREATE PROCEDURE get_product_details(IN product_id INT)
BEGIN
    SELECT * FROM products WHERE pid = product_id;
END //

/*
EXPLANATION:
product_id is the IN parameter.
INT is the data type of the parameter.
*/

-- Calling Procedure
CALL get_product_details(1);
-- This will retrieve details for the product with ID 1.

/* 
EXPLANATION:
-> CREATE PROCEDURE get_product_details(IN product_id INT): This statement defines a procedure named get_product_details
with an IN parameter product_id of type INT.
-> BEGIN and END: These keywords mark the beginning and end of the procedure's body, respectively.
-> SELECT * FROM products WHERE pid = product_id;: This is the SQL query inside the procedure that selects product details
based on the product_id parameter.
-> CALL get_product_details(3); This statement calls the procedure get_product_details with the argument 3, 
which is the product ID to retrieve details for.
*/



-- OUT
/* 
This OUT is a  part of procedures
 OUT  OUT parameters in MySQL stored procedures allow you to return values from a procedure. 
These values can be accessed by the calling program after the procedure execution. 
*/

/* 
~ Syntax
 CREATE PROCEDURE procedure_name(OUT parameter_name data_type)
 BEGIN
    -- Procedure logic using parameter_name
 END;
*/

-- Create the procedure to get product count using OUT
DELIMITER //
CREATE PROCEDURE get_product_count(OUT product_count INT)
BEGIN
    SELECT COUNT(*) INTO product_count FROM products;
END //
/*
EXPLANATION:
product_count is the OUT parameter.
INT is the data type of the parameter.
*/

-- Calling the OUT Procedure
CALL get_product_count(@product_count);
SELECT @product_count as product_count;
/*
call -> Using @product_count to store the result
select-> Accessing the variable using @product_count
*/


/*
EXPLANATION:
-> CREATE PROCEDURE get_product_count(OUT product_count INT): This statement defines a procedure named get_product_count with an
 OUT parameter product_count of type INT.
-> BEGIN and END: These keywords mark the beginning and end of the procedures body, respectively.
-> SELECT COUNT(*) INTO product_count FROM products;: This is the SQL query inside the procedure that calculates the 
total number of products and stores it in the product_count variable.
-> CALL get_product_count(@count);: This statement calls the procedure get_product_count and 
passes the OUT parameter. The result is stored in the variable @count.
*/



-- CURSOR
/*
	1. Purpose:
		- Cursors in SQL are used to retrieve and process rows one by one from the result set of a query.
	2. Declaration:
		- Cursors are declared using the DECLARE CURSOR statement, specifying the SELECT query whose result set will be processed.
	3. Opening:
		- A cursor must be opened using the OPEN statement before fetching rows.
		- Opening a cursor positions the cursor before the first row.
	4. Fetching:
		- Rows from the result set are fetched one by one using the FETCH statement.
		- Each fetch operation advances the cursor to the next row in the result set.
	5. Closing:
		- After processing all rows, the cursor should be closed using the CLOSE statement.
		- Closing a cursor releases the resources associated with the result set and frees memory.
*/

/*
~ SYNTAX:

DECLARE cursor_name CURSOR FOR
SELECT column1, column2, ... 
FROM table_name 
WHERE condition;

OPEN cursor_name;

FETCH cursor_name INTO variable1, variable2, ...;

WHILE (condition) DO
    -- Process fetched row here
    -- Use fetched values stored in variables
    FETCH cursor_name INTO variable1, variable2, ...;
END WHILE;

CLOSE cursor_name;
*/

/*There exists two type cursor based on their creation by user or not one is user-defined and other is pre-defined */

/*
~ User-Defined Cursors:
	1. Purpose:
		- User-defined cursors are declared by the user to process rows retrieved from a query result set.
		- They are particularly useful when you need to perform custom operations on individual rows.

	2. Declaration:
		- User-defined cursors are declared using the DECLARE CURSOR statement, specifying the SELECT query whose result set will be processed.
		- This allows the user to define custom logic for fetching and processing rows.

	3. Opening, Fetching, and Closing:
		- User-defined cursors follow a similar process of opening, fetching, and closing as predefined cursors.
		- After declaring and opening the cursor, the user fetches rows one by one and processes them as needed.
		- Finally, the cursor is closed to release resources.
*/

-- EXAMPLE:
-- To calculate the number of customers
DELIMITER //
DECLARE @customer_count INT;

SELECT @customer_count = COUNT(*)
FROM customer;

PRINT 'Number of customers: ' + CAST(@customer_count AS VARCHAR(10));
DELIMITER ;

/* 
EXPLANATION:
-> The script starts with a SELECT statement.
-> The COUNT(*) function counts the number of rows in the customer table.
-> It concatenates the string 'Number of customers: ' with the count obtained from the COUNT(*) function.
-> The CAST() function is used to convert the count value to a string.
-> The result of the SELECT statement is the concatenated string, shows the number of customers.
*/


/* 
~ Pre-defined Cursors:
	1. Purpose:
		- Predefined cursors are system-defined cursors provided by the DBMS.
		- They are often associated with built-in functions or stored procedures that return result sets.

	2. Usage:
		-Predefined cursors are commonly used with predefined functions or procedures to process result sets returned by these functions.
		- Examples of predefined cursors include cursors used with aggregate functions like COUNT(), SUM(), or with system-defined stored procedures.
*/

-- EXAMPLE:
-- To calculate the sum of prices for all HP laptops
DELIMITER //
DECLARE @total_price INT;

SELECT @total_price = SUM(price)
FROM products
WHERE pname = 'HP Laptop';
PRINT 'Total price of all HP Laptops: ' + CAST(@total_price AS VARCHAR(20));
DELIMITER ;

/*
EXPLANATION:
-> DECLARE @total_price INT; This line declares a variable @total_price of type integer. 
   This variable will hold the sum of prices of all HP laptops.
-> SELECT @total_price = SUM(price) FROM products WHERE pname = 'HP Laptop';
   This query calculates the sum of prices (SUM(price)) of all products where the product name (pname) is 'HP Laptop'. The result is stored in the variable @total_price.
-> PRINT 'Total price of all HP Laptops: ' + CAST(@total_price AS VARCHAR(20));
   This line prints a message indicating the total price of all HP laptops. It concatenates the string 'Total price of all HP Laptops: ' with the value of @total_price converted to a string using CAST()
*/


-- PRACTICE QUESTIONS 

-- 1. PROCEDURES

-- Ques 1. Write a query to create a procedure that selects all dishes from the 'dishes' table, and call the procedure to retrieve all dishes.
-- Ques 2. Write a query to create a function that calculates the total revenue from the 'orders' and 'payment' tables for completed orders, and call the function to get the total revenue.
-- Ques 3. Write a query to create a procedure with an IN parameter to retrieve details of a specific dish based on the dish ID passed as a parameter. Call the procedure for dish ID 5.
-- Ques 4. Write a query to create a procedure with an OUT parameter to get the count of dishes in the 'dishes' table, store it in a variable, and select the variable to display the count.


USE rapido;

-- Answer 1:
DELIMITER $$
CREATE PROCEDURE select_all_dishes()
BEGIN
    SELECT * FROM dishes;
END$$
DELIMITER ;

CALL select_all_dishes();


-- Answer 2:
DELIMITER $$
CREATE FUNCTION get_total_revenue()
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE total_revenue DECIMAL(10,2);
    SELECT SUM(p.amount) INTO total_revenue
    FROM payments p
    INNER JOIN orders o ON p.oid = o.oid
    WHERE p.status = 'completed';
    RETURN total_revenue;
END$$
DELIMITER ;

SELECT get_total_revenue();


-- Answer 3:
DELIMITER $$
CREATE PROCEDURE get_dish_details(IN dish_id INT)
BEGIN
    SELECT * FROM dishes WHERE did = dish_id;
END$$
DELIMITER ;

CALL get_dish_details(5);


-- Answer 4:
DELIMITER $$
CREATE PROCEDURE get_dish_count(OUT total_count INT)
BEGIN
    SELECT COUNT(*) INTO total_count FROM dishes;
END$$
DELIMITER ;

CALL get_dish_count(@count);
SELECT @count AS total_dishes;
