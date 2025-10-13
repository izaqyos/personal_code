// tests/setup.js
const fs = require('fs');
const util = require('util');
const path = require('path');
const { execSync } = require('child_process');

// Path relative to project root, not tests/ directory
const logFilePath = path.join(__dirname, '..', 'test_verbose_results.log');
let logStream;

// Store original console methods
const originalConsole = {
    log: console.log,
    error: console.error,
    warn: console.warn,
};

// Helper function to format console arguments like console.log does
const formatArgs = (args) => {
    return util.format(...args) + '\n';
};

function checkDockerRunning() {
  try {
    // Try to execute a simple Docker command
    execSync('docker ps', { stdio: 'ignore' });
    return true;
  } catch (error) {
    console.error('\x1b[31m%s\x1b[0m', 'ERROR: Docker is not running!');
    console.error('\x1b[33m%s\x1b[0m', 'Please start Docker and make sure the database container is running:');
    console.error('\x1b[36m%s\x1b[0m', '  docker compose up -d db');
    console.error('\x1b[33m%s\x1b[0m', 'Alternatively, use the provided script to run tests:');
    console.error('\x1b[36m%s\x1b[0m', '  ./run_tests.sh [--unit] [--integration] [--coverage]');
    return false;
  }
}

beforeAll(async () => {
  if (process.env.RUN_INTEGRATION_TESTS === 'true') {
    if (!checkDockerRunning()) {
      throw new Error('Docker must be running for integration tests');
    }
  }

  try {
    // Create/Truncate the log file and open a write stream
    logStream = fs.createWriteStream(logFilePath, { flags: 'w' });

    // Mock console methods to write to the file stream
    jest.spyOn(console, 'log').mockImplementation((...args) => {
        if (logStream) {
            logStream.write(formatArgs(args));
        }
        // Optionally call original if you want output *and* file logging
        // originalConsole.log.apply(console, args);
    });
    jest.spyOn(console, 'error').mockImplementation((...args) => {
        if (logStream) {
            logStream.write('[ERROR] ' + formatArgs(args)); // Add prefix for errors
        }
        // originalConsole.error.apply(console, args);
    });
    jest.spyOn(console, 'warn').mockImplementation((...args) => {
        // DEBUG: Check if this mock is being hit
        originalConsole.log('>>> console.warn MOCK CALLED <<<'); 
        if (logStream) {
            logStream.write('[WARN] ' + formatArgs(args)); // Add prefix for warnings
        }
        // originalConsole.warn.apply(console, args);
    });

  } catch (err) {
      // Log setup error using the original console
      originalConsole.error('Error setting up test log file:', err);
  }
});

afterAll((done) => {
  // Restore original console methods
  jest.restoreAllMocks();

  // Close the file stream
  if (logStream) {
    logStream.end(() => {
        originalConsole.log(`\nVerbose test logs written to: ${logFilePath}`);
        done(); // Signal Jest that async operation is complete
    });
  } else {
      done();
  }
}); 