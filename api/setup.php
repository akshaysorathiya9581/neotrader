<?php
header("Content-Type: text/html; charset=UTF-8");
?>
<!DOCTYPE html>
<html>
<head>
    <title>NeoTrader Database Setup</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .success { color: green; background: #e8f5e9; padding: 10px; border-radius: 5px; margin: 10px 0; }
        .error { color: red; background: #ffebee; padding: 10px; border-radius: 5px; margin: 10px 0; }
        .info { color: #1565c0; background: #e3f2fd; padding: 10px; border-radius: 5px; margin: 10px 0; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background: #f5f5f5; }
        h1 { color: #333; }
        .btn { display: inline-block; padding: 10px 20px; background: #1976d2; color: white; text-decoration: none; border-radius: 5px; margin: 10px 5px 10px 0; }
        .btn:hover { background: #1565c0; }
    </style>
</head>
<body>
    <h1>NeoTrader Database Setup</h1>
    
    <?php
    // Step 1: Check MySQL connection
    echo "<h2>Step 1: Database Connection</h2>";
    
    try {
        $pdo = new PDO("mysql:host=localhost", "root", "");
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        echo '<div class="success">MySQL connection successful!</div>';
    } catch (PDOException $e) {
        echo '<div class="error">MySQL connection failed: ' . $e->getMessage() . '</div>';
        echo '<div class="info">Make sure XAMPP MySQL is running!</div>';
        exit;
    }

    // Step 2: Create database
    echo "<h2>Step 2: Create Database</h2>";
    
    try {
        $pdo->exec("CREATE DATABASE IF NOT EXISTS neotrader CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
        echo '<div class="success">Database "neotrader" created/verified!</div>';
    } catch (PDOException $e) {
        echo '<div class="error">Failed to create database: ' . $e->getMessage() . '</div>';
        exit;
    }

    // Step 3: Create users table
    echo "<h2>Step 3: Create Users Table</h2>";
    
    try {
        $pdo->exec("USE neotrader");
        
        $createTableSQL = "
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            full_name VARCHAR(255) DEFAULT NULL,
            phone VARCHAR(20) DEFAULT NULL,
            status_select VARCHAR(50) DEFAULT NULL,
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
        
        $pdo->exec($createTableSQL);
        echo '<div class="success">Users table created/verified!</div>';
    } catch (PDOException $e) {
        echo '<div class="error">Failed to create table: ' . $e->getMessage() . '</div>';
        exit;
    }

    // Step 4: Seed users
    echo "<h2>Step 4: Seed Demo Users</h2>";
    
    $users = [
        ['email' => 'admin@neotrader.com', 'password' => 'Admin@123', 'full_name' => 'Admin User', 'phone' => '+1234567890', 'status_select' => 'Professional'],
        ['email' => 'demo@neotrader.com', 'password' => 'Demo@123', 'full_name' => 'Demo User', 'phone' => '+1987654321', 'status_select' => 'Trader'],
        ['email' => 'test@neotrader.com', 'password' => 'Test@123', 'full_name' => 'Test User', 'phone' => '+1122334455', 'status_select' => 'Beginner'],
    ];

    $createdUsers = [];
    
    foreach ($users as $user) {
        try {
            $checkStmt = $pdo->prepare("SELECT id FROM users WHERE email = ?");
            $checkStmt->execute([$user['email']]);
            
            if ($checkStmt->rowCount() == 0) {
                $hashedPassword = password_hash($user['password'], PASSWORD_DEFAULT);
                $insertStmt = $pdo->prepare("INSERT INTO users (email, password, full_name, phone, status_select, status) VALUES (?, ?, ?, ?, ?, 'active')");
                $insertStmt->execute([$user['email'], $hashedPassword, $user['full_name'], $user['phone'], $user['status_select']]);
                $createdUsers[] = $user;
            }
        } catch (PDOException $e) {
            echo '<div class="error">Error creating user ' . $user['email'] . ': ' . $e->getMessage() . '</div>';
        }
    }

    if (count($createdUsers) > 0) {
        echo '<div class="success">Created ' . count($createdUsers) . ' new user(s)!</div>';
    } else {
        echo '<div class="info">All demo users already exist.</div>';
    }

    // Display login credentials
    echo "<h2>Login Credentials</h2>";
    echo '<table>';
    echo '<tr><th>Email</th><th>Password</th><th>Role</th></tr>';
    foreach ($users as $user) {
        echo '<tr><td>' . $user['email'] . '</td><td>' . $user['password'] . '</td><td>' . $user['status_select'] . '</td></tr>';
    }
    echo '</table>';

    echo '<div class="success"><strong>Setup Complete!</strong> You can now use the application.</div>';
    
    echo '<a href="/neotrader/" class="btn">Go to Dashboard</a>';
    echo '<a href="/neotrader/login" class="btn">Go to Login</a>';
    ?>
</body>
</html>
