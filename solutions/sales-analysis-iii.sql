SELECT product_id, product_name
FROM product
JOIN sales
USING(product_id)
-- WHERE sale_date BETWEEN '2019-01-01' AND '2019-03-31'
GROUP BY product_id
HAVING MIN(sale_date) >= '2019-01-01' AND MAX(sale_date) <= '2019-03-31'
