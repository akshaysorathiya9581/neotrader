<?php
/**
 * NeoTrader Authentication API
 * Handles login and user profile
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

// Database configuration
$host = 'localhost';
$dbname = 'neotrader';
$username = 'root';
$password = '';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8mb4", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Database connection failed']);
    exit;
}

// Simple JWT functions (for production, use a proper JWT library)
function generateToken($userId) {
    $header = base64_encode(json_encode(['typ' => 'JWT', 'alg' => 'HS256']));
    $payload = base64_encode(json_encode([
        'user_id' => $userId,
        'exp' => time() + (24 * 60 * 60) // 24 hours
    ]));
    $secret = 'your-secret-key-change-in-production';
    $signature = base64_encode(hash_hmac('sha256', "$header.$payload", $secret, true));
    return "$header.$payload.$signature";
}

function verifyToken($token) {
    $parts = explode('.', $token);
    if (count($parts) !== 3) return null;
    
    $payload = json_decode(base64_decode($parts[1]), true);
    if (!$payload || $payload['exp'] < time()) return null;
    
    return $payload['user_id'];
}

function getAuthUser($pdo) {
    $headers = getallheaders();
    $authHeader = $headers['Authorization'] ?? '';
    
    if (!preg_match('/Bearer\s+(.*)$/i', $authHeader, $matches)) {
        return null;
    }
    
    $userId = verifyToken($matches[1]);
    if (!$userId) return null;
    
    $stmt = $pdo->prepare("SELECT id, name, email, role, plan_id, phone, avatar FROM users WHERE id = ? AND is_active = 1");
    $stmt->execute([$userId]);
    return $stmt->fetch(PDO::FETCH_ASSOC);
}

// Get request path
$requestUri = $_SERVER['REQUEST_URI'];
$path = parse_url($requestUri, PHP_URL_PATH);
$path = str_replace('/api/', '', $path);

// Route handling
switch ($path) {
    // ==========================================
    // LOGIN - POST /api/auth/login
    // ==========================================
    case 'auth/login':
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            http_response_code(405);
            echo json_encode(['error' => 'Method not allowed']);
            exit;
        }
        
        $input = json_decode(file_get_contents('php://input'), true);
        $email = $input['email'] ?? '';
        $password = $input['password'] ?? '';
        
        if (empty($email) || empty($password)) {
            http_response_code(400);
            echo json_encode(['error' => 'Email and password required']);
            exit;
        }
        
        // Find user by email
        $stmt = $pdo->prepare("SELECT * FROM users WHERE email = ? AND is_active = 1");
        $stmt->execute([$email]);
        $user = $stmt->fetch(PDO::FETCH_ASSOC);
        
        if (!$user || !password_verify($password, $user['password'])) {
            http_response_code(401);
            echo json_encode(['error' => 'Invalid credentials']);
            exit;
        }
        
        // Generate token
        $token = generateToken($user['id']);
        
        // Return user data with role
        echo json_encode([
            'success' => true,
            'token' => $token,
            'user' => [
                'id' => $user['id'],
                'name' => $user['name'],
                'email' => $user['email'],
                'role' => $user['role'],  // 'superadmin' or 'user'
                'plan_id' => $user['plan_id'],
                'phone' => $user['phone'],
                'avatar' => $user['avatar']
            ]
        ]);
        break;
    
    // ==========================================
    // GET USER PROFILE - GET /api/user/profile
    // ==========================================
    case 'user/profile':
        if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
            http_response_code(405);
            echo json_encode(['error' => 'Method not allowed']);
            exit;
        }
        
        $user = getAuthUser($pdo);
        if (!$user) {
            http_response_code(401);
            echo json_encode(['error' => 'Unauthorized']);
            exit;
        }
        
        // Get user's current plan details if subscribed
        $plan = null;
        if ($user['plan_id']) {
            $stmt = $pdo->prepare("SELECT * FROM subscription_plans WHERE id = ?");
            $stmt->execute([$user['plan_id']]);
            $plan = $stmt->fetch(PDO::FETCH_ASSOC);
        }
        
        echo json_encode([
            'id' => $user['id'],
            'name' => $user['name'],
            'email' => $user['email'],
            'role' => $user['role'],  // This determines if user is superadmin
            'plan_id' => $user['plan_id'],
            'phone' => $user['phone'],
            'avatar' => $user['avatar'],
            'plan' => $plan
        ]);
        break;
    
    // ==========================================
    // CHECK IF SUPERADMIN - GET /api/user/is-admin
    // ==========================================
    case 'user/is-admin':
        $user = getAuthUser($pdo);
        if (!$user) {
            http_response_code(401);
            echo json_encode(['error' => 'Unauthorized']);
            exit;
        }
        
        echo json_encode([
            'is_admin' => $user['role'] === 'superadmin'
        ]);
        break;
    
    // ==========================================
    // GET ALL PLANS - GET /api/plans
    // ==========================================
    case 'plans':
        $stmt = $pdo->query("SELECT * FROM subscription_plans WHERE is_active = 1 ORDER BY price ASC");
        $plans = $stmt->fetchAll(PDO::FETCH_ASSOC);
        
        // Decode JSON fields
        foreach ($plans as &$plan) {
            $plan['features'] = json_decode($plan['features'], true);
            $plan['module_ids'] = json_decode($plan['module_ids'], true);
        }
        
        echo json_encode($plans);
        break;
    
    // ==========================================
    // GET ALL MODULES - GET /api/modules
    // ==========================================
    case 'modules':
        $stmt = $pdo->query("SELECT * FROM modules WHERE is_active = 1 ORDER BY category, name");
        echo json_encode($stmt->fetchAll(PDO::FETCH_ASSOC));
        break;
    
    // ==========================================
    // SUBSCRIBE TO PLAN - POST /api/subscribe
    // ==========================================
    case 'subscribe':
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            http_response_code(405);
            echo json_encode(['error' => 'Method not allowed']);
            exit;
        }
        
        $user = getAuthUser($pdo);
        if (!$user) {
            http_response_code(401);
            echo json_encode(['error' => 'Unauthorized']);
            exit;
        }
        
        $input = json_decode(file_get_contents('php://input'), true);
        $planId = $input['plan_id'] ?? null;
        
        if (!$planId) {
            http_response_code(400);
            echo json_encode(['error' => 'Plan ID required']);
            exit;
        }
        
        // Update user's plan
        $stmt = $pdo->prepare("UPDATE users SET plan_id = ? WHERE id = ?");
        $stmt->execute([$planId, $user['id']]);
        
        // Record subscription
        $stmt = $pdo->prepare("SELECT price FROM subscription_plans WHERE id = ?");
        $stmt->execute([$planId]);
        $plan = $stmt->fetch(PDO::FETCH_ASSOC);
        
        $stmt = $pdo->prepare("INSERT INTO user_subscriptions (user_id, plan_id, start_date, end_date, amount_paid, status) VALUES (?, ?, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 1 MONTH), ?, 'active')");
        $stmt->execute([$user['id'], $planId, $plan['price']]);
        
        echo json_encode(['success' => true, 'message' => 'Subscription successful']);
        break;
    
    default:
        http_response_code(404);
        echo json_encode(['error' => 'Endpoint not found']);
}
