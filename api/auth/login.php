<?php
require_once '../config/database.php';

$database = new Database();
$db = $database->getConnection();

$data = json_decode(file_get_contents("php://input"));

if (!empty($data->email) && !empty($data->password)) {
    $email = htmlspecialchars(strip_tags($data->email));
    $password = $data->password;

    $query = "SELECT id, email, password, full_name, phone, status, created_at FROM users WHERE email = :email LIMIT 1";
    $stmt = $db->prepare($query);
    $stmt->bindParam(":email", $email);
    $stmt->execute();

    if ($stmt->rowCount() > 0) {
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        
        if (password_verify($password, $row['password'])) {
            if ($row['status'] !== 'active') {
                http_response_code(401);
                echo json_encode([
                    "success" => false,
                    "message" => "Account is not active. Please contact support."
                ]);
                exit();
            }

            // Generate a simple token (in production, use JWT)
            $token = bin2hex(random_bytes(32));
            
            // Update last login
            $updateQuery = "UPDATE users SET last_login = NOW(), auth_token = :token WHERE id = :id";
            $updateStmt = $db->prepare($updateQuery);
            $updateStmt->bindParam(":token", $token);
            $updateStmt->bindParam(":id", $row['id']);
            $updateStmt->execute();

            http_response_code(200);
            echo json_encode([
                "success" => true,
                "message" => "Login successful",
                "data" => [
                    "id" => $row['id'],
                    "email" => $row['email'],
                    "full_name" => $row['full_name'],
                    "phone" => $row['phone'],
                    "token" => $token
                ]
            ]);
        } else {
            http_response_code(401);
            echo json_encode([
                "success" => false,
                "message" => "Invalid email or password"
            ]);
        }
    } else {
        http_response_code(401);
        echo json_encode([
            "success" => false,
            "message" => "Invalid email or password"
        ]);
    }
} else {
    http_response_code(400);
    echo json_encode([
        "success" => false,
        "message" => "Email and password are required"
    ]);
}
?>
