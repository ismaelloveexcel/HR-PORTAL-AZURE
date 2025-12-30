const { Pool } = require('pg');

// Database connection configuration
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
});

// Test connection
pool.on('connect', () => {
  console.log('✅ Connected to PostgreSQL database');
});

pool.on('error', (err) => {
  console.error('❌ Unexpected error on idle client', err);
  process.exit(-1);
});

// Query helper function
const query = (text, params) => pool.query(text, params);

// Initialize database schema
const initDatabase = async () => {
  try {
    console.log('📊 Initializing database schema...');

    // Read and execute schema file
    const fs = require('fs');
    const path = require('path');
    const schemaPath = path.join(__dirname, 'schema.sql');

    if (fs.existsSync(schemaPath)) {
      const schema = fs.readFileSync(schemaPath, 'utf8');
      await pool.query(schema);
      console.log('✅ Database schema initialized successfully');
    } else {
      console.log('⚠️  Schema file not found, skipping initialization');
    }
  } catch (error) {
    console.error('❌ Error initializing database:', error);
    throw error;
  }
};

module.exports = {
  query,
  pool,
  initDatabase
};
