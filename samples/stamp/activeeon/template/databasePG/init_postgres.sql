-- Create users
CREATE USER rm WITH PASSWORD 'rm';
CREATE USER scheduler WITH PASSWORD 'scheduler';
CREATE USER catalog WITH PASSWORD 'catalog';

-- Creating empty databases
CREATE DATABASE rm OWNER scheduler;
CREATE DATABASE scheduler OWNER scheduler;
CREATE DATABASE catalog OWNER scheduler;

-- Grant access
GRANT CONNECT ON DATABASE scheduler TO scheduler;
GRANT USAGE ON SCHEMA public TO scheduler;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO scheduler;
GRANT CONNECT ON DATABASE rm TO rm;
GRANT USAGE ON SCHEMA public TO rm;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO rm;
GRANT CONNECT ON DATABASE catalog TO catalog;
GRANT USAGE ON SCHEMA public TO catalog;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO catalog;
ALTER SYSTEM SET max_connections ='150'
