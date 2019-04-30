CREATE DATABASE citygo_malaga;
CREATE USER citygo WITH PASSWORD '5X6sdoq0!?az=v2aSX';
ALTER ROLE citygo SET client_encoding TO 'utf8';
ALTER ROLE citygo SET default_transaction_isolation TO 'read committed';
ALTER ROLE citygo SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE citygo_malaga TO citygo;
\q
Exit
