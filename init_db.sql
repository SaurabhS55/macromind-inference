-- Create database
CREATE DATABASE IF NOT EXISTS macrodb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE macrodb;

-- Create foods table with global nutrition cache
CREATE TABLE IF NOT EXISTS nutrition_lookup (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    
    normalized_name VARCHAR(255) NOT NULL UNIQUE,
    display_name VARCHAR(255) NOT NULL,
    
    -- Nutrition per 100g (industry standard)
    calories FLOAT NOT NULL DEFAULT 0,
    protein FLOAT NOT NULL DEFAULT 0,
    carbs FLOAT NOT NULL DEFAULT 0,
    fats FLOAT NOT NULL DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_normalized_name (normalized_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
