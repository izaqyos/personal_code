const { execSync } = require('child_process');

console.log('Checking test environment...');

// Check if Docker is running
try {
  const dockerPs = execSync('docker ps').toString();
  console.log('✅ Docker is running');
  
  // Check if PostgreSQL container is running
  if (dockerPs.includes('postgres') || dockerPs.includes('toymcp_db')) {
    console.log('✅ PostgreSQL container is running');
  } else {
    console.error('❌ PostgreSQL container is not running');
    console.error('Please start the database with: docker compose up -d db');
    process.exit(1);
  }
} catch (error) {
  console.error('❌ Docker is not running or not accessible');
  console.error('Please start Docker and run: docker compose up -d db');
  process.exit(1);
}

// Instead of direct DB connection check, try using pg_isready via docker
try {
  console.log('Checking database availability...');
  const containerName = execSync('docker ps --format "{{.Names}}" | grep postgres').toString().trim();
  
  if (containerName) {
    const checkResult = execSync(`docker exec ${containerName} pg_isready -h localhost`).toString();
    if (checkResult.includes('accepting connections')) {
      console.log('✅ Database is accepting connections');
    } else {
      console.error('❌ Database is not accepting connections');
      console.error('Please check database logs: docker logs ' + containerName);
      process.exit(1);
    }
  }
} catch (error) {
  console.warn('⚠️  Could not check database availability directly');
  console.warn('Database may not be ready yet, but Docker container is running');
  console.log('Continuing with tests...');
}

console.log('Environment check complete'); 