-- ==========================================
-- SQL DDL Statements
-- ==========================================

-- ==========================================
-- RESET (Drop tables in reverse order of dependency)
-- ==========================================
DROP TABLE IF EXISTS students;

-- ==========================================
-- CREATE Tables (in order of dependency)
-- ==========================================

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    student_number VARCHAR(50) NOT NULL UNIQUE
);
