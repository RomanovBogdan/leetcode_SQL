SELECT sell_date,
    COUNT(DISTINCT product) num_sold,
    GROUP_CONCAT(DISTINCT product ORDER BY product) products
FROM activities
-- JOIN activities a2 USING (sell_date)
GROUP BY sell_date
ORDER BY sell_date