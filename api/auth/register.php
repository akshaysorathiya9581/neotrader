<?php
require_once '../config/database.php';

$database = new Database();
$db = $database->getConnection();

$data = json_decode(file_get_contents("php://input"));

if (!empty($data->email) && !empty($data->password) && !empty($data->phone) && !empty($data->status)) {
    $email = htmlspecialchars(strip_tags($data->email));
    $phone = htmlspecialchars(strip_tags($data->phone));
    $status_select = htmlspecialchars(strip_tags($data->status));
    $password = $data->password;
    $confirm_password = $data->confirm_password ?? '';

    // Validate email format
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        http_response_code(400);
        echo json_encode([
            "success" => false,
            "message" => "Invalid email format"
        ]);
        exit();
    }

    // Validate password strength
    if (strlen($password) < 8) {
        http_response_code(400);
        echo json_encode([
            "success" => false,
            "message" => "Password must be at least 8 characters"
        ]);
        exit();
    }

    if (!preg_match('/[A-Z]/', $password)) {
        http_response_code(400);
        echo json_encode([
            "success" => false,
            "message" => "Password must contain at least one uppercase letter"
        ]);
        exit();
    }

    if (!preg_match('/[a-z]/', $password)) {
        http_response_code(400);
        echo json_encode([
            "success" => false,
            "message" => "Password must contain at least one lowercase letter"
        ]);
        exit();
    }

    if (!preg_match('/[0-9]/', $password)) {
        http_response_code(400);
        echo json_encode([
            "success" => false,
            "message" => "Password must contain at least one number"
        ]);
        exit();
    }

    if (!preg_match('/[!@#$%^&*(),.?":{}|<>]/', $password)) {
        http_response_code(400);
        echo json_encode([
            "success" => false,
            "message" => "Password must contain at least one special character"
        ]);
        exit();
    }

    // Check if passwords match
    if ($password !== $confirm_password) {
        http_response_code(400);
        echo json_encode([
            "success" => false,
            "message" => "Passwords do not match"
        ]);
        exit();
    }

    // Check if email already exists
    $checkQuery = "SELECT id FROM users WHERE email = :email LIMIT 1";
    $checkStmt = $db->prepare($checkQuery);
    $checkStmt->bindParam(":email", $email);
    $checkStmt->execute();

    if ($checkStmt->rowCount() > 0) {
        http_response_code(409);
        echo json_encode([
            "success" => false,
            "message" => "Email already registered"
        ]);
        exit();
    }

    // Hash password
    $hashed_password = password_hash($password, PASSWORD_DEFAULT);

    // Insert new user
    $query = "INSERT INTO users (email, password, phone, status_select, status, created_at) VALUES (:email, :password, :phone, :status_select, 'active', NOW())";
    $stmt = $db->prepare($query);
    $stmt->bindParam(":email", $email);
    $stmt->bindParam(":password", $hashed_password);
    $stmt->bindParam(":phone", $phone);
    $stmt->bindParam(":status_select", $status_select);

    if ($stmt->execute()) {
        $userId = $db->lastInsertId();
        
        http_response_code(201);
        echo json_encode([
            "success" => true,
            "message" => "Registration successful! You can now login.",
            "data" => [
                "id" => $userId,
                "email" => $email
            ]
        ]);
    } else {
        http_response_code(500);
        echo json_encode([
            "success" => false,
            "message" => "Registration failed. Please try again."
        ]);
    }
} else {
    http_response_code(400);
    echo json_encode([
        "success" => false,
        "message" => "All fields are required (email, password, phone, status)"
    ]);
}
?>
