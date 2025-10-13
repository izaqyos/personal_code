const request = require('supertest');
const passport = require('passport'); // Import passport

// Mock dependencies *before* importing the app
const mockRouter = jest.fn(); // Simple mock function
mockRouter._shouldThrowError = false; // Control flag

jest.mock('../../src/mcp_router', () => {
    // Return a middleware function that uses the mockRouter
    return (req, res, next) => {
        if (mockRouter._shouldThrowError) {
            next(new Error('Simulated Router Error'));
        } else {
            // If not throwing, just call next() to simulate passing through
            // without actually handling the request like the real router would.
            next();
        }
    };
});

// Mock the database initialization as it's not needed for these error tests
jest.mock('../../src/db', () => ({
    initializeDatabase: jest.fn().mockResolvedValue(undefined), // Mock successful init
    // We don't need pool or query for these specific tests
}));

// Mock passport.authenticate
// This mock will ensure that for any call to passport.authenticate,
// it immediately calls the next middleware, effectively bypassing auth
// and attaching a mock user to req.user.
jest.mock('passport', () => ({
    ...jest.requireActual('passport'), // Import and retain default behavior
    authenticate: jest.fn((strategy, options) => { // Mock the authenticate function
        return (req, res, next) => {
            req.user = { id: 1, username: 'testuser' }; // Mock a user object
            next(); // Proceed to the next middleware (your actual route handler or error)
        };
    }),
    initialize: jest.fn(() => (req, res, next) => next()), // Mock initialize if needed
}));

// Now import the app, which will use the mocked dependencies
const app = require('../../src/server');
// We don't need to require the mock directly anymore, the mock is active via jest.mock

// Test Suite
describe('Server Error Handling Middleware', () => {

    beforeEach(() => {
        // Reset mock state before each test
        mockRouter._shouldThrowError = false; // Reset the flag on the mock itself
        // Add this to the beforeEach section
        app.use('/rpc', (req, res, next) => {
            // Skip auth middleware for this test
            req.user = { id: 1, username: 'test' }; // Mock authenticated user
            next();
        }, mockRouter);
        // Clear mock history before each test
        passport.authenticate.mockClear();
        if (passport.initialize) passport.initialize.mockClear();
    });

    it('should use the global error handler for unhandled errors from subsequent middleware/routers', async () => {
        // This test expects an error to bypass auth and hit the global error handler.
        // The mock above should allow this.
        
        // Make sure your mockRouter setup correctly throws an error that would be caught
        // by the global error handler.
        mockRouter.get('/error-route', (req, res, next) => {
            next(new Error('Simulated Router Error')); // Simulate an error
        });

        const dummyRequest = { jsonrpc: "2.0", method: "some.method", id: 1 };

        const res = await request(app)
            .get('/rpc/error-route') // Make sure this path will trigger the error in mockRouter
                                     // And that mockRouter is mounted under /rpc or a relevant path
            .send(dummyRequest);

        expect(res.status).toBe(500); 
        // If you have a specific JSON error structure from your global handler:
        // expect(res.body.error.message).toContain('Simulated Router Error');
    });

    it('should use the dedicated syntax error handler for invalid JSON bodies', async () => {
        const res = await request(app)
            .post('/rpc') // CORRECTED: Or any route that uses express.json()
            .set('Content-Type', 'application/json')
            .send('{"invalid": json, ...') // Send malformed JSON
            .expect('Content-Type', /json/) // Expect JSON error response
            .expect(200); // Expect 200 OK (per JSON-RPC spec for Parse Error)

        expect(res.body.jsonrpc).toBe('2.0');
        expect(res.body.error).toBeDefined();
        expect(res.body.error.code).toBe(-32700); // Parse error
        expect(res.body.error.message).toContain('Parse error: Invalid JSON received.');
        expect(res.body.id).toBeNull();
    });

    // Add more tests here if needed for other specific error middleware scenarios
});

// Or mock the auth middleware directly:
// Ensure this path is correct for your project structure.
// If your auth middleware is in, for example, src/auth/auth_middleware.js
// then the path would be '../auth/auth_middleware'
jest.mock('../middleware/auth', () => ({ // Or the correct path
    authenticateToken: (req, res, next) => {
        req.user = { id: 1, username: 'test' }; // Mock an authenticated user
        next();
    }
})); 