-- Create n8n database for automation workflows
CREATE DATABASE n8n;

-- Grant permissions to postgres user
GRANT ALL PRIVILEGES ON DATABASE n8n TO postgres;

-- Connect to n8n database and create necessary extensions
\c n8n;

-- Create extensions that n8n might need
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
