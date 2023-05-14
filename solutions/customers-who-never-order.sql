-- Write your MySQL query statement below
SELECT name Customers
FROM customers
LEFT JOIN orders
ON customers.id = orders.customerId
WHERE customerId IS NULL
