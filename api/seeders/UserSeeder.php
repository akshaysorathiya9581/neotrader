<?php
require_once __DIR__ . '/../config/database.php';

echo "=== NeoTrader User Seeder ===\n\n";

$database = new Database();
$db = $database->getConnection();

if (!$db) {
    echo "ERROR: Could not connect to database.\n";
    echo "Make sure MySQL is running and 'neotrader' database exists.\n";
    exit(1);
}

echo "Connected to database successfully!\n\n";

// Create users table if not exists
$createTableSQL = "
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) DEFAULT NULL,
    phone VARCHAR(20) DEFAULT NULL,
    status_select VARCHAR(50) DEFAULT NULL COMMENT 'User selected status from dropdown',
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    auth_token VARCHAR(255) DEFAULT NULL,
    last_login DATETIME DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_status (status),
    INDEX idx_auth_token (auth_token)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
";

try {
    $db->exec($createTableSQL);
    echo "Users table created/verified successfully!\n\n";
} catch (PDOException $e) {
    echo "Error creating table: " . $e->getMessage() . "\n";
    exit(1);
}

// Seed users
$users = [
    [
        'email' => 'admin@neotrader.com',
        'password' => 'Admin@123',
        'full_name' => 'Admin User',
        'phone' => '+1234567890',
        'status_select' => 'Professional',
        'status' => 'active'
    ],
    [
        'email' => 'demo@neotrader.com',
        'password' => 'Demo@123',
        'full_name' => 'Demo User',
        'phone' => '+1987654321',
        'status_select' => 'Trader',
        'status' => 'active'
    ],
    [
        'email' => 'test@neotrader.com',
        'password' => 'Test@123',
        'full_name' => 'Test User',
        'phone' => '+1122334455',
        'status_select' => 'Beginner',
        'status' => 'active'
    ]
];

echo "Seeding users...\n";
echo str_repeat("-", 50) . "\n";

foreach ($users as $user) {
    // Check if user already exists
    $checkQuery = "SELECT id FROM users WHERE email = :email LIMIT 1";
    $checkStmt = $db->prepare($checkQuery);
    $checkStmt->bindParam(":email", $user['email']);
    $checkStmt->execute();

    if ($checkStmt->rowCount() > 0) {
        echo "User '{$user['email']}' already exists, skipping...\n";
        continue;
    }

    // Hash password
    $hashedPassword = password_hash($user['password'], PASSWORD_DEFAULT);

    // Insert user
    $insertQuery = "INSERT INTO users (email, password, full_name, phone, status_select, status, created_at) 
                    VALUES (:email, :password, :full_name, :phone, :status_select, :status, NOW())";
    $insertStmt = $db->prepare($insertQuery);
    $insertStmt->bindParam(":email", $user['email']);
    $insertStmt->bindParam(":password", $hashedPassword);
    $insertStmt->bindParam(":full_name", $user['full_name']);
    $insertStmt->bindParam(":phone", $user['phone']);
    $insertStmt->bindParam(":status_select", $user['status_select']);
    $insertStmt->bindParam(":status", $user['status']);

    if ($insertStmt->execute()) {
        echo "Created user: {$user['email']} (Password: {$user['password']})\n";
    } else {
        echo "Failed to create user: {$user['email']}\n";
    }
}

echo str_repeat("-", 50) . "\n\n";
echo "=== Seeding Complete! ===\n\n";
echo "You can now login with:\n";
echo "  Email: admin@neotrader.com | Password: Admin@123\n";
echo "  Email: demo@neotrader.com  | Password: Demo@123\n";
echo "  Email: test@neotrader.com  | Password: Test@123\n";
?>
