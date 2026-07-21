import sqlite3
import pandas as pd

conn = sqlite3.connect('data.sqlite')

# Part 1: Join and Filter
query_1_1 = """
SELECT e.firstName, e.lastName, e.jobTitle
FROM employees e
JOIN offices o ON e.officeCode = o.officeCode
WHERE o.city = 'Boston';
"""
df_1_1 = pd.read_sql(query_1_1, conn)

query_1_2 = """
SELECT o.officeCode, o.city
FROM offices o
LEFT JOIN employees e ON o.officeCode = e.officeCode
GROUP BY o.officeCode, o.city
HAVING COUNT(e.employeeNumber) = 0;
"""
df_1_2 = pd.read_sql(query_1_2, conn)

# Part 2: Type of Join
query_2_1 = """
SELECT e.firstName, e.lastName, o.city, o.state
FROM employees e
LEFT JOIN offices o ON e.officeCode = o.officeCode
ORDER BY e.firstName ASC, e.lastName ASC;
"""
df_2_1 = pd.read_sql(query_2_1, conn)

query_2_2 = """
SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
FROM customers c
LEFT JOIN orders o ON c.customerNumber = o.customerNumber
WHERE o.orderNumber IS NULL
ORDER BY c.contactLastName ASC;
"""
df_2_2 = pd.read_sql(query_2_2, conn)

# Part 3: Built-In Function
query_3_1 = """
SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate
FROM customers c
JOIN payments p ON c.customerNumber = p.customerNumber
ORDER BY CAST(p.amount AS REAL) DESC;
"""
df_3_1 = pd.read_sql(query_3_1, conn)

# Part 4: Joining and Grouping
query_4_1 = """
SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS num_customers
FROM employees e
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber, e.firstName, e.lastName
HAVING AVG(c.creditLimit) > 90000
ORDER BY num_customers DESC;
"""
df_4_1 = pd.read_sql(query_4_1, conn)

query_4_2 = """
SELECT p.productName, COUNT(od.orderNumber) AS numorders, SUM(od.quantityOrdered) AS totalunits
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
GROUP BY p.productCode, p.productName
ORDER BY totalunits DESC;
"""
df_4_2 = pd.read_sql(query_4_2, conn)

# Part 5: Multiple Joins
query_5_1 = """
SELECT p.productName, p.productCode, COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
JOIN orders o ON od.orderNumber = o.orderNumber
GROUP BY p.productCode, p.productName
ORDER BY numpurchasers DESC;
"""
df_5_1 = pd.read_sql(query_5_1, conn)

query_5_2 = """
SELECT COUNT(c.customerNumber) AS n_customers, o.officeCode, o.city
FROM offices o
JOIN employees e ON o.officeCode = e.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode, o.city;
"""
df_5_2 = pd.read_sql(query_5_2, conn)

# Part 6: Subquery
query_6_1 = """
SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, off.city, off.officeCode
FROM employees e
JOIN offices off ON e.officeCode = off.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders o ON c.customerNumber = o.customerNumber
JOIN orderdetails od ON o.orderNumber = od.orderNumber
WHERE od.productCode IN (
    SELECT od_sub.productCode
    FROM orderdetails od_sub
    JOIN orders o_sub ON od_sub.orderNumber = o_sub.orderNumber
    GROUP BY od_sub.productCode
    HAVING COUNT(DISTINCT o_sub.customerNumber) < 20
);
"""
df_6_1 = pd.read_sql(query_6_1, conn)

conn.close()