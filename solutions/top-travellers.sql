SELECT users.name, IFNULL(SUM(rides.distance), 0) travelled_distance
FROM users
LEFT JOIN rides
ON users.id = rides.user_id
GROUP BY users.id
ORDER BY travelled_distance DESC, users.name
