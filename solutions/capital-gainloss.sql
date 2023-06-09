SELECT stock_name, SUM(CASE
  WHEN operation = 'Sell' THEN price
  ELSE -price END) capital_gain_loss
FROM stocks
GROUP BY stock_name
