SELECT DISTINCT event_day day,
    emp_id,
    SUM(out_time - in_time) total_time
FROM employees
GROUP BY  emp_id, event_day
ORDER BY event_day
