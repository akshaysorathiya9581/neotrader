CREATE DATABASE IF NOT EXISTS neotrader;
USE neotrader;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    phone VARCHAR(20),
    status_select VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    auth_token VARCHAR(255),
    last_login DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Demo user (password: Demo@123)
INSERT IGNORE INTO users (email, password, full_name, phone, status_select, status) 
VALUES ('demo@neotrader.com', '$2y$10$YourHashHere', 'Demo User', '+1234567890', 'Trader', 'active');
