import pg from 'pg';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

// Create a connection pool
const pool = new pg.Pool({
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'postgres',
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    database: process.env.DB_NAME || 'cargo_smart',
});

// Test the connection
pool.connect((err, client, release) => {
    if (err) {
        console.error('Error connecting to the database:', err.stack);
    } else {
        console.log('Successfully connected to database');
        release();
    }
});

// Export query helper
export const query = (text, params) => pool.query(text, params);

// Export pool for direct use if needed
export default pool;
