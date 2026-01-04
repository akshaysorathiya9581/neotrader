<?php
// Simple and fast database initialization
error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "Initializing NeoTrader Database...\n";

try {
    // Connect without database first
    $pdo = new PDO("mysql:host=localhost", "root", "", [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_TIMEOUT => 5
    ]);
    
    // Create database
    $pdo->exec("CREATE DATABASE IF NOT EXISTS neotrader");
    $pdo->exec("USE neotrader");
    
    // Create users table
    $pdo->exec("
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
        )
    ");
    
    // Insert demo user (password: Demo@123)
    $hash = password_hash('Demo@123', PASSWORD_DEFAULT);
    $pdo->exec("INSERT IGNORE INTO users (email, password, full_name, phone, status_select, status) 
                VALUES ('demo@neotrader.com', '$hash', 'Demo User', '+1234567890', 'Trader', 'active')");
    
    // Insert admin user (password: Admin@123)
    $hash2 = password_hash('Admin@123', PASSWORD_DEFAULT);
    $pdo->exec("INSERT IGNORE INTO users (email, password, full_name, phone, status_select, status) 
                VALUES ('admin@neotrader.com', '$hash2', 'Admin User', '+1234567890', 'Professional', 'active')");
    
    echo "SUCCESS! Database ready.\n\n";
    echo "Login credentials:\n";
    echo "- demo@neotrader.com / Demo@123\n";
    echo "- admin@neotrader.com / Admin@123\n";
    
} catch (PDOException $e) {
    echo "ERROR: " . $e->getMessage() . "\n";
}
?>
