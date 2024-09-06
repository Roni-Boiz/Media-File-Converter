CREATE USER IF NOT EXISTS 'auth_user'@'localhost' IDENTIFIED BY 'authuser123';

CREATE DATABASE IF NOT EXISTS auth;

GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

use auth;

CREATE TABLE IF NOT EXISTS user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO user (email, password)
SELECT 'don@email.com', 'admin1234'
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM user WHERE email = 'don@email.com'
);
