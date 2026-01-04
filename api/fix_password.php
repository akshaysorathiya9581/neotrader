<?php
require_once 'config/database.php';

header("Content-Type: application/json");

$database = new Database();
$db = $database->getConnection();

// Generate correct password hash for Demo@123
$password = "Demo@123";
$hashed = password_hash($password, PASSWORD_DEFAULT);

// Update demo user password
$query = "UPDATE users SET password = :password WHERE email = 'demo@neotrader.com'";
$stmt = $db->prepare($query);
$stmt->bindParam(":password", $hashed);
$stmt->execute();

// Also update admin password
$adminPassword = password_hash("Admin@123", PASSWORD_DEFAULT);
$query2 = "UPDATE users SET password = :password WHERE email = 'admin@neotrader.com'";
$stmt2 = $db->prepare($query2);
$stmt2->bindParam(":password", $adminPassword);
$stmt2->execute();

echo json_encode([
    "success" => true,
    "message" => "Passwords updated successfully",
    "demo_hash" => $hashed
]);
?>
