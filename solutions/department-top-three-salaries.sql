SELECT
    d.name department,
    e1.name employee,
    e1.salary salary
FROM
    employee e1
    JOIN employee e2
    JOIN department d ON e1.departmentid = e2.departmentid
    AND e1.salary <= e2.salary
    AND d.id = e2.departmentid
GROUP BY
    1, 2, 3
HAVING
    COUNT(distinct(e2.salary)) <= 3