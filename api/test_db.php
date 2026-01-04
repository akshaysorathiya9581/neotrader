<?php
require_once 'config/database.php';

header("Content-Type: application/json");

$database = new Database();
$db = $database->getConnection();

$query = "SELECT id, email, full_name, status FROM users";
$stmt = $db->prepare($query);
$stmt->execute();

$users = $stmt->fetchAll(PDO::FETCH_ASSOC);

echo json_encode([
    "success" => true,
    "users" => $users
]);
?>
