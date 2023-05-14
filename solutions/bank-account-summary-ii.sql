SELECT name, SUM(amount) balance
FROM users
JOIN transactions
USING(account)
GROUP BY account
HAVING balance > 10000