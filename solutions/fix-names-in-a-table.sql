SELECT user_id,
    CONCAT(UPPER(LEFT(name,1)),
    LOWER(RIGHT(name, LENGTH(name)-1))) name
FROM users
ORDER BY user_id
