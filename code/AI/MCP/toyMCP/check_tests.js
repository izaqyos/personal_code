// A simple script to verify test setup
const { execSync } = require('child_process');
const fs = require('fs');

console.log('Checking test environment...');

// Check Docker
try {
  execSync('docker ps', { stdio: 'pipe' });
  console.log('✅ Docker is running');
  
  // Check if the PostgreSQL container is running
  const dockerPs = execSync('docker ps').toString();
  if (dockerPs.includes('postgres') || dockerPs.includes('toymcp_db')) {
    console.log('✅ PostgreSQL container is running');
  } else {
    console.log('❌ PostgreSQL container is not running. Run: docker compose up -d db');
    process.exit(1);
  }
} catch (error) {
  console.log('❌ Docker is not running. Please start Docker.');
  process.exit(1);
}

// Check database connectivity
try {
  const { Pool } = require('pg');
  const pool = new Pool();
  
  // Add a timeout for the test
  const connectPromise = pool.connect();
  const timeoutPromise = new Promise((_, reject) => 
    setTimeout(() => reject(new Error('Connection timeout')), 5000)
  );
  
  Promise.race([connectPromise, timeoutPromise])
    .then(client => {
      console.log('✅ Database connection successful');
      client.release();
      pool.end();
    })
    .catch(err => {
      console.log('❌ Database connection failed:', err.message);
      process.exit(1);
    });
} catch (error) {
  console.log('❌ Error checking database:', error.message);
  process.exit(1);
}

console.log('Environment check complete'); 