
-- Creating empty databases
drop database if exists rm; create database rm;
drop database if exists scheduler; create database scheduler;
drop database if exists catalog; create database catalog;

-- Create users
CREATE USER IF NOT EXISTS 'rm'@'localhost' IDENTIFIED BY 'rm';
CREATE USER IF NOT EXISTS 'rm'@'%' IDENTIFIED BY 'rm';
CREATE USER IF NOT EXISTS 'scheduler'@'localhost' IDENTIFIED BY 'scheduler';
CREATE USER IF NOT EXISTS 'scheduler'@'%' IDENTIFIED BY 'scheduler';
CREATE USER IF NOT EXISTS 'catalog'@'localhost' IDENTIFIED BY 'catalog';
CREATE USER IF NOT EXISTS 'catalog'@'%' IDENTIFIED BY 'catalog';
CREATE USER IF NOT EXISTS 'scheduler-api'@'localhost' IDENTIFIED BY 'scheduler-api';
CREATE USER IF NOT EXISTS 'scheduler-api'@'%' IDENTIFIED BY 'scheduler-api';
CREATE USER IF NOT EXISTS 'job-planner'@'localhost' IDENTIFIED BY 'job-planner';
CREATE USER IF NOT EXISTS 'job-planner'@'%' IDENTIFIED BY 'job-planner';

-- Grant access
GRANT ALL PRIVILEGES ON rm.* TO 'rm'@'localhost';
GRANT ALL PRIVILEGES ON rm.* TO 'rm'@'%';
GRANT ALL PRIVILEGES ON scheduler.* TO 'scheduler'@'localhost';
GRANT ALL PRIVILEGES ON scheduler.* TO 'scheduler'@'%';
GRANT ALL PRIVILEGES ON catalog.* TO 'catalog'@'localhost';
GRANT ALL PRIVILEGES ON catalog.* TO 'catalog'@'%';
GRANT ALL PRIVILEGES ON scheduler.* TO 'scheduler-api'@'localhost';
GRANT ALL PRIVILEGES ON scheduler.* TO 'scheduler-api'@'%';
GRANT ALL PRIVILEGES ON scheduler.* TO 'job-planner'@'localhost';
GRANT ALL PRIVILEGES ON scheduler.* TO 'job-planner'@'%';
FLUSH PRIVILEGES;
