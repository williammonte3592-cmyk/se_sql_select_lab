# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd


# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Return the first and last names for all employees in Boston
df_boston = pd.read_sql("""
    SELECT e.firstName, e.lastName
    FROM employees e
    JOIN offices o ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston'
""", conn)

# STEP 2
# Are there any offices that have zero employees?
df_zero_emp = pd.read_sql("""
    SELECT officeCode, city
    FROM offices
    WHERE officeCode NOT IN (SELECT officeCode FROM employees)
""", conn)

# STEP 3
# Return employees first name and last name along with the city and state of the office
df_employee = pd.read_sql("""
    SELECT e.firstName, e.lastName, o.city, o.state
    FROM employees e
    LEFT JOIN offices o ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName
""", conn)

# STEP 4
# Return customer contact info for customers with no orders
df_contacts = pd.read_sql("""
    SELECT contactFirstName, contactLastName, phone, salesRepEmployeeNumber
    FROM customers
    WHERE customerNumber NOT IN (SELECT customerNumber FROM orders)
    ORDER BY contactLastName
""", conn)

# STEP 5
# Return customer contacts with payment amounts, sorted by payment amount descending
df_payment = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate
    FROM customers c
    JOIN payments p ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC
""", conn)

# STEP 6
# Return employees whose customers have average credit limit over 90k
df_credit = pd.read_sql("""
    SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(*) as num_customers
    FROM employees e
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY num_customers DESC
""", conn)

# STEP 7
# Return product name, order count, and total units sold
df_product_sold = pd.read_sql("""
    SELECT p.productName, COUNT(o.orderNumber) as numorders, SUM(od.quantityOrdered) as totalunits
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    JOIN orders o ON od.orderNumber = o.orderNumber
    GROUP BY p.productName
    ORDER BY totalunits DESC
""", conn)

# STEP 8
# Return product name, code, and number of unique customers who ordered each product
df_total_customers = pd.read_sql("""
    SELECT p.productName, p.productCode, COUNT(DISTINCT o.customerNumber) as numpurchasers
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    JOIN orders o ON od.orderNumber = o.orderNumber
    GROUP BY p.productName
    ORDER BY numpurchasers DESC
""", conn)

# STEP 9
# Return count of customers per office
df_customers = pd.read_sql("""
    SELECT o.officeCode, o.city, COUNT(c.customerNumber) as n_customers
    FROM offices o
    JOIN employees e ON o.officeCode = e.officeCode
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode
""", conn)

# STEP 10
# Return employees who sold products ordered by fewer than 20 customers
df_under_20 = pd.read_sql("""
    SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, o.city, o.officeCode
    FROM employees e
    JOIN offices o ON e.officeCode = o.officeCode
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders ord ON c.customerNumber = ord.customerNumber
    JOIN orderdetails od ON ord.orderNumber = od.orderNumber
    WHERE od.productCode IN (
        SELECT productCode
        FROM orderdetails od2
        JOIN orders ord2 ON od2.orderNumber = ord2.orderNumber
        GROUP BY od2.productCode
        HAVING COUNT(DISTINCT ord2.customerNumber) < 20
    )
    ORDER BY e.lastName, e.firstName
""", conn)

# Close the connection
conn.close()