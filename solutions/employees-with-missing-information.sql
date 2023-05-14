WITH t1 AS (SELECT *
FROM employees
LEFT JOIN salaries
USING (employee_id)
UNION ALL
SELECT *
FROM employees
RIGHT JOIN salaries
USING (employee_id))

SELECT employee_id
FROM t1
WHERE name IS NULL OR salary IS NULL
ORDER BY employee_id