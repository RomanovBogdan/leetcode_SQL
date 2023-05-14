-- Write your MySQL query statement below
SELECT d.name Department, e.name Employee, e.salary Salary
FROM employee e
JOIN department d
ON e.departmentId = d.id
WHERE (departmentId, salary) IN (SELECT departmentId,MAX(salary) FROM Employee GROUP BY departmentId);
