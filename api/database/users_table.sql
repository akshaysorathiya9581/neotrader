-- =============================================
-- USERS TABLE STRUCTURE FOR NEOTRADER
-- =============================================

-- Users table with role column
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(100) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,
  `role` ENUM('superadmin', 'user') NOT NULL DEFAULT 'user',
  `plan_id` INT(11) DEFAULT NULL,
  `phone` VARCHAR(20) DEFAULT NULL,
  `avatar` VARCHAR(255) DEFAULT NULL,
  `email_verified_at` TIMESTAMP NULL DEFAULT NULL,
  `is_active` TINYINT(1) NOT NULL DEFAULT 1,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_email` (`email`),
  KEY `idx_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Subscription Plans table
CREATE TABLE IF NOT EXISTS `subscription_plans` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `duration` ENUM('month', 'quarter', 'year') NOT NULL DEFAULT 'month',
  `description` TEXT,
  `features` JSON,
  `module_ids` JSON,
  `color` VARCHAR(20) DEFAULT 'primary',
  `is_popular` TINYINT(1) DEFAULT 0,
  `is_active` TINYINT(1) DEFAULT 1,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Modules table
CREATE TABLE IF NOT EXISTS `modules` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `path` VARCHAR(100) NOT NULL,
  `icon` VARCHAR(50) DEFAULT 'tabler-apps',
  `category` VARCHAR(50) NOT NULL,
  `is_active` TINYINT(1) DEFAULT 1,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- User subscriptions history
CREATE TABLE IF NOT EXISTS `user_subscriptions` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `plan_id` INT(11) NOT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `amount_paid` DECIMAL(10,2) NOT NULL,
  `payment_id` VARCHAR(100),
  `status` ENUM('active', 'expired', 'cancelled') DEFAULT 'active',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_plan_id` (`plan_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`plan_id`) REFERENCES `subscription_plans`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================
-- INSERT DEFAULT DATA
-- =============================================

-- Insert SuperAdmin user (password: admin123)
INSERT INTO `users` (`name`, `email`, `password`, `role`, `plan_id`) VALUES
('Super Admin', 'admin@neotrader.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'superadmin', NULL),
('John Doe', 'john@example.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'user', 2),
('Jane Smith', 'jane@example.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'user', 1);

-- Insert default subscription plans
INSERT INTO `subscription_plans` (`name`, `price`, `duration`, `description`, `features`, `module_ids`, `color`, `is_popular`) VALUES
('Basic', 999.00, 'month', 'Essential trading tools for beginners', '["Dashboard Access", "Stock Query Window", "Basic Charts"]', '[1, 2, 3]', 'info', 0),
('Professional', 2499.00, 'month', 'Advanced tools for active traders', '["All Basic Features", "Technical Indicators", "Pivot Analysis", "Candlestick Patterns", "Real-time Charts"]', '[1, 2, 3, 4, 5, 6, 7]', 'success', 1),
('Enterprise', 4999.00, 'month', 'Complete suite for professional traders', '["All Professional Features", "Expert Alerts", "Ichimoku Dashboard", "Options Trading", "Priority Support"]', '[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]', 'warning', 0);

-- Insert default modules
INSERT INTO `modules` (`name`, `path`, `icon`, `category`) VALUES
('Dashboard', '/dashboard', 'tabler-layout-dashboard', 'core'),
('Stock Query', '/query-window', 'tabler-search', 'core'),
('Real-time Charts', '/my-markets/charts', 'tabler-chart-line', 'core'),
('ADX Trends', '/technical/adx-trends', 'tabler-trending-up', 'technical'),
('RSI Trends', '/technical/rsi-trends', 'tabler-chart-dots', 'technical'),
('ATR Trends', '/technical/atr-trends', 'tabler-activity', 'technical'),
('Key Indicators', '/technical/key-indicators', 'tabler-gauge', 'technical'),
('Fibonacci Pivots', '/pivots/fibonacci-pivots', 'tabler-spiral', 'pivots'),
('Camarilla Pivots', '/pivots/camarilla-pivots', 'tabler-arrows-split', 'pivots'),
('CPR Analysis', '/pivots/cpr', 'tabler-chart-bar', 'pivots'),
('Candlestick Patterns', '/candlestick', 'tabler-chart-candle', 'candlestick'),
('Heikin Ashi', '/candlestick/heikin-ashi', 'tabler-chart-candle-filled', 'candlestick'),
('Expert Alerts', '/expert-alerts', 'tabler-bell-ringing', 'alerts'),
('Ichimoku Dashboard', '/ichimoku', 'tabler-cloud', 'advanced'),
('Options Trade', '/trades/options-trade', 'tabler-replace', 'trades'),
('Intraday Trades', '/trades/intraday-trades', 'tabler-clock', 'trades');
