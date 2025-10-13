# Testing Guide

## Running Tests

The recommended way to run tests is using the provided script:

```bash
# Run all tests with proper setup
chmod +x run_tests.sh
./run_tests.sh

# Run only unit tests
./run_tests.sh unit

# Run only integration tests
./run_tests.sh integration
```

This script will:
1. Ensure Docker is running
2. Start the PostgreSQL database container if needed
3. Wait for the database to initialize
4. Run the specified tests

## Common Test Failures

### Database Connection Issues
- **Symptoms**: Tests fail with `Pool.connect()` errors
- **Solutions**:
  - Make sure Docker is running
  - Start the database container: `docker compose up -d db`
  - Give the database time to initialize (5-10 seconds)

### Authentication Token Issues
- **Symptoms**: Tests fail with `Authentication token not obtained in beforeAll hook`
- **Solutions**:
  - Ensure the database container is running (auth needs the database)
  - Check that test user credentials match the expected values

### Unit Test Issues
- **Symptoms**: SQL statement or mock function call mismatches
- **Solutions**:
  - These tests are sensitive to database schema changes
  - Update the tests if you've modified the database schema

## Manual Test Running

If you prefer to run tests manually:

1. Start the database:
   ```bash
   docker compose up -d db
   ```

2. Run the tests:
   ```bash
   npm test
   ```

## Troubleshooting

If tests are consistently failing:

1. Try clean database restart:
   ```bash
   docker compose down
   docker compose up -d db
   ```

2. Check database logs:
   ```bash
   docker logs toymcp_db
   ```

3. Run individual test files:
   ```bash
   npx jest tests/unit_tests/specific_test_file.js
   ``` 